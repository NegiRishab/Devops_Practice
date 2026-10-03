from io import BytesIO
import subprocess
import unittest
import urllib.error
from unittest.mock import MagicMock, patch

from health import check, NoRedirect
from recovery import recover_server, server_recovery_needed


class HealthTests(unittest.TestCase):
    @patch("health.urllib.request.build_opener")
    def test_status_and_body_must_both_match(self, build):
        response = MagicMock()
        response.code = 200
        response.read.return_value = b"service ready"
        build.return_value.open.return_value = response
        self.assertTrue(check("http://example.test", 200, "ready")[0])
        self.assertFalse(check("http://example.test", 200, "missing")[0])
        response.code = 503
        self.assertFalse(check("http://example.test")[0])

    @patch("health.urllib.request.build_opener")
    def test_http_error_status_is_checked(self, build):
        build.return_value.open.side_effect = urllib.error.HTTPError(
            "http://example.test", 503, "unavailable", {}, BytesIO(b"down"))
        healthy, detail = check("http://example.test")
        self.assertFalse(healthy)
        self.assertIn("503", detail)

    @patch("health.urllib.request.build_opener")
    def test_timeout_is_unhealthy(self, build):
        build.return_value.open.side_effect = TimeoutError()
        self.assertFalse(check("http://example.test")[0])

    def test_redirects_are_not_followed(self):
        self.assertIsNone(NoRedirect().redirect_request(None, None, 302, "Found", {}, "http://other.test"))


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.config = {"linode_id": 123, "ssh_host": "192.0.2.5", "website_url": "http://192.0.2.5/health",
                       "host_port": 80, "expected_status": 200, "expected_text": "", "http_timeout": 2}

    @patch("recovery.Linode")
    def test_running_instance_is_rebooted(self, api):
        api.return_value.request.return_value = {"ipv4": ["192.0.2.5"], "status": "running"}
        self.assertEqual(recover_server(self.config), "Linode reboot requested")
        api.return_value.request.assert_called_with("POST", "linode/instances/123/reboot", {})

    @patch("recovery.Linode")
    def test_offline_instance_is_booted(self, api):
        api.return_value.request.return_value = {"ipv4": ["192.0.2.5"], "status": "offline"}
        self.assertEqual(recover_server(self.config), "Linode boot requested")
        api.return_value.request.assert_called_with("POST", "linode/instances/123/boot", {})

    @patch("recovery.Linode")
    def test_transitioning_instance_is_left_alone(self, api):
        api.return_value.request.return_value = {"ipv4": ["192.0.2.5"], "status": "booting"}
        recover_server(self.config)
        self.assertEqual(api.return_value.request.call_count, 1)

    @patch("recovery.Linode")
    def test_wrong_instance_is_never_rebooted(self, api):
        api.return_value.request.return_value = {"ipv4": ["192.0.2.6"], "status": "running"}
        with self.assertRaises(ValueError):
            recover_server(self.config)
        self.assertEqual(api.return_value.request.call_count, 1)

    @patch("recovery.run_remote")
    def test_bad_ssh_credentials_do_not_trigger_reboot(self, remote):
        remote.return_value = subprocess.CompletedProcess([], 255, "", "Permission denied (publickey)")
        self.assertFalse(server_recovery_needed(self.config)[0])

    @patch("recovery.run_remote")
    def test_network_timeout_can_trigger_server_recovery(self, remote):
        remote.return_value = subprocess.CompletedProcess([], 255, "", "connect to host: Connection timed out")
        self.assertTrue(server_recovery_needed(self.config)[0])

    @patch("recovery.run_remote")
    def test_missing_diagnostic_script_does_not_trigger_reboot(self, remote):
        remote.return_value = subprocess.CompletedProcess([], 2, "", "No such file")
        self.assertFalse(server_recovery_needed(self.config)[0])


if __name__ == "__main__":
    unittest.main()
