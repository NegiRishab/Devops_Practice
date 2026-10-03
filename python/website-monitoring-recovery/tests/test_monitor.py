import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from common import load_config
from monitor import Monitor


class MonitorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.config = load_config(Path(__file__).resolve().parents[1] / "config.example.json")
        self.config.update(state_file=str(Path(self.temp.name) / "state.json"),
                           enable_server_recovery=True, linode_id=123,
                           failure_threshold=3, recovery_cooldown=10, boot_grace=30,
                           server_recovery_cooldown=60)
        self.check = self.mock("monitor.check", return_value=(False, "HTTP 503"))
        self.email = self.mock("monitor.send_email", return_value=True)
        self.restart = self.mock("monitor.restart_container", return_value="Restart requested")
        self.diagnose = self.mock("monitor.server_recovery_needed", return_value=(True, "Local failure"))
        self.reboot = self.mock("monitor.recover_server", return_value="Reboot requested")
        self.monitor = Monitor(self.config)

    def mock(self, target, **kwargs):
        patcher = patch(target, **kwargs)
        self.addCleanup(patcher.stop)
        return patcher.start()

    def fail_to_threshold(self):
        for now in (0, 1, 2):
            self.monitor.tick(now)

    def test_transient_failure_does_not_recover_or_alert(self):
        self.monitor.tick(0)
        self.check.return_value = True, "HTTP 200"
        self.monitor.tick(1)
        self.restart.assert_not_called()
        self.email.assert_not_called()
        self.assertEqual(self.monitor.state["failures"], 0)

    def test_threshold_cooldown_and_recovery_budgets(self):
        self.fail_to_threshold()
        self.assertEqual(self.restart.call_count, 1)
        self.monitor.tick(11)
        self.assertEqual(self.restart.call_count, 1)
        self.monitor.tick(12)
        self.assertEqual(self.restart.call_count, 2)
        self.monitor.tick(22)
        self.reboot.assert_called_once()
        for now in (23, 52, 1000):
            self.monitor.tick(now)
        self.assertEqual(self.restart.call_count, 2)
        self.reboot.assert_called_once()

    def test_budgets_survive_monitor_restart(self):
        self.fail_to_threshold()
        self.monitor = Monitor(self.config)
        self.monitor.tick(3)
        self.assertEqual(self.restart.call_count, 1)
        self.monitor.tick(12)
        self.monitor.tick(22)
        self.monitor = Monitor(self.config)
        self.monitor.tick(1000)
        self.reboot.assert_called_once()

    def test_smtp_failure_does_not_block_recovery_and_is_retried(self):
        self.email.return_value = False
        self.fail_to_threshold()
        self.restart.assert_called_once()
        self.assertTrue(self.monitor.state["pending_emails"])
        self.email.return_value = True
        self.monitor.tick(3)
        self.assertEqual(self.monitor.state["pending_emails"], [])

    def test_recovery_email_only_once(self):
        self.fail_to_threshold()
        self.check.return_value = True, "HTTP 200"
        self.monitor.tick(3)
        self.assertEqual(self.email.call_args.args[1], "Website recovered")
        calls = self.email.call_count
        self.monitor.tick(4)
        self.assertEqual(self.email.call_count, calls)

    def test_remote_local_health_prevents_reboot(self):
        self.diagnose.return_value = False, "Healthy locally"
        self.fail_to_threshold()
        self.monitor.tick(12)
        self.monitor.tick(22)
        self.reboot.assert_not_called()

    def test_server_recovery_disabled(self):
        self.config["enable_server_recovery"] = False
        self.fail_to_threshold()
        self.monitor.tick(12)
        self.monitor.tick(22)
        self.reboot.assert_not_called()

    def test_intent_is_saved_before_server_operation(self):
        def reboot(config):
            state = json.loads(Path(config["state_file"]).read_text())
            self.assertTrue(state["server_attempted"])
            return "Reboot requested"
        self.reboot.side_effect = reboot
        self.fail_to_threshold()
        self.monitor.tick(12)
        self.monitor.tick(22)
        self.reboot.assert_called_once()

    def test_failed_server_request_is_not_repeated(self):
        self.reboot.side_effect = RuntimeError("API unreachable")
        self.fail_to_threshold()
        self.monitor.tick(12)
        self.monitor.tick(22)
        self.monitor.tick(1000)
        self.reboot.assert_called_once()

    def test_server_cooldown_survives_new_incident(self):
        self.fail_to_threshold()
        self.monitor.tick(12)
        self.monitor.tick(22)
        self.check.return_value = True, "HTTP 200"
        self.monitor.tick(23)
        self.check.return_value = False, "HTTP 503"
        for now in (24, 25, 26, 36, 46):
            self.monitor.tick(now)
        self.reboot.assert_called_once()
        self.monitor.tick(82)
        self.assertEqual(self.reboot.call_count, 2)

    def test_corrupt_state_fails_closed(self):
        Path(self.config["state_file"]).write_text('{}')
        with self.assertRaises(ValueError):
            Monitor(self.config)
        self.reboot.assert_not_called()

    def test_persistence_failure_prevents_actions(self):
        with patch("monitor.save_json", side_effect=OSError("disk full")):
            with self.assertRaises(OSError):
                self.monitor.tick(0)
        self.restart.assert_not_called()


if __name__ == "__main__":
    unittest.main()
