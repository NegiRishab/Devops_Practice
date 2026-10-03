import json
from pathlib import Path
import smtplib
import tempfile
import unittest
from unittest.mock import patch

from common import load_config
from notify import send_email
from provision import main


class ProvisionTests(unittest.TestCase):
    @patch("provision.time.sleep")
    @patch("provision.getpass.getpass", return_value="test-password-only")
    @patch("provision.Linode")
    def test_firewall_is_attached_before_boot_and_resume_does_not_create_duplicates(self, api, password, sleep):
        with tempfile.TemporaryDirectory() as directory:
            key = Path(directory) / "test.pub"
            key.write_text("ssh-ed25519 fake-key-for-mocked-api")
            output = Path(directory) / "deployment.json"
            argv = ["provision.py", "--region", "test-region", "--admin-cidr", "192.0.2.10/32",
                    "--ssh-public-key", str(key), "--output", str(output)]
            api.return_value.request.side_effect = [
                {"data": [], "pages": 1},
                {"id": 123, "ipv4": ["192.0.2.5"]},
                {"id": 456},
                {"id": 123, "ipv4": ["192.0.2.5"], "status": "offline"},
                {},
                {"id": 123, "ipv4": ["192.0.2.5"], "status": "running"}]
            with patch("sys.argv", argv):
                main()
            calls = api.return_value.request.call_args_list
            self.assertFalse(calls[1].args[2]["booted"])
            self.assertEqual(calls[2].args[:2], ("POST", "networking/firewalls"))
            self.assertEqual(calls[4].args[:2], ("POST", "linode/instances/123/boot"))
            self.assertEqual(json.loads(output.read_text())["firewall_id"], 456)
            self.assertEqual(output.stat().st_mode & 0o777, 0o600)
            api.return_value.request.reset_mock()
            api.return_value.request.side_effect = [
                {"id": 123, "ipv4": ["192.0.2.5"], "status": "running"}]
            with patch("sys.argv", argv):
                main()
            api.return_value.request.assert_called_once_with("GET", "linode/instances/123")


class NotificationTests(unittest.TestCase):
    def setUp(self):
        self.config = load_config(Path(__file__).resolve().parents[1] / "config.example.json")

    @patch.dict("os.environ", {"SMTP_USERNAME": "test-user", "SMTP_PASSWORD": "test-password"})
    @patch("notify.smtplib.SMTP")
    def test_tls_is_enabled_before_login_and_send(self, smtp):
        smtp.return_value.send_message.return_value = {}
        self.assertTrue(send_email(self.config, "Test", "Example"))
        names = [call[0] for call in smtp.return_value.method_calls]
        self.assertLess(names.index("starttls"), names.index("login"))
        self.assertLess(names.index("login"), names.index("send_message"))

    @patch("notify.smtplib.SMTP", side_effect=smtplib.SMTPConnectError(421, b"Unavailable"))
    def test_smtp_error_returns_failure_instead_of_crashing(self, smtp):
        self.assertFalse(send_email(self.config, "Test", "Example"))


if __name__ == "__main__":
    unittest.main()
