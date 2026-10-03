"""Configuration, private state files, and the Linode API (stdlib only)."""
import json
import os
import re
from pathlib import Path
import tempfile
import urllib.error
import urllib.request
from urllib.parse import urlparse


def load_config(path):
    path = Path(path).resolve()
    config = json.loads(path.read_text())
    defaults = json.loads(Path(__file__).with_name("config.example.json").read_text())
    unknown = set(config) - set(defaults)
    if unknown:
        raise ValueError(f"Unknown configuration keys: {sorted(unknown)}")
    config = defaults | config
    if not isinstance(config["image"], str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._/@:-]*", config["image"]):
        raise ValueError("Invalid container image reference")
    for key in ("http_timeout", "check_interval", "failure_threshold",
                "recovery_cooldown", "boot_grace", "server_recovery_cooldown", "max_container_restarts",
                "host_port", "container_port", "smtp_port"):
        if type(config[key]) is not int or config[key] <= 0:
            raise ValueError(f"{key} must be a positive integer")
    for key in ("host_port", "container_port", "smtp_port"):
        if config[key] > 65535:
            raise ValueError(f"Invalid {key}")
    if type(config["expected_status"]) is not int or not 100 <= config["expected_status"] <= 599:
        raise ValueError("expected_status must be an HTTP status code")
    if not isinstance(config["expected_text"], str):
        raise ValueError("expected_text must be a string")
    url = urlparse(config["website_url"])
    if url.scheme not in ("http", "https") or not url.hostname or url.username or url.password:
        raise ValueError("website_url must be an HTTP(S) URL without credentials")
    if type(config["enable_server_recovery"]) is not bool:
        raise ValueError("enable_server_recovery must be true or false")
    if type(config["linode_id"]) is not int or config["linode_id"] < 0:
        raise ValueError("linode_id must be a nonnegative integer")
    if config["enable_server_recovery"] and not config["linode_id"]:
        raise ValueError("Server recovery requires linode_id")
    if config["smtp_security"] not in ("starttls", "ssl"):
        raise ValueError("smtp_security must be starttls or ssl")
    if not isinstance(config["email_to"], list) or not config["email_to"]:
        raise ValueError("email_to must be a nonempty list")
    for key in ("ssh_host", "ssh_user"):
        value = config[key]
        if not isinstance(value, str) or not value or value.startswith("-") or any(c.isspace() for c in value):
            raise ValueError(f"Invalid {key}")
    for key in ("ssh_key", "ssh_known_hosts", "state_file"):
        value = Path(config[key]).expanduser()
        config[key] = str(value if value.is_absolute() else path.parent / value)
    return config


def save_json(path, value):
    """Atomic, owner-only writes; fail closed if persistence is unavailable."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(dir=path.parent)
    try:
        with os.fdopen(fd, "w") as stream:
            json.dump(value, stream, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp, path)
        directory = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


class Linode:
    def __init__(self):
        self.token = os.environ.get("LINODE_TOKEN", "")
        if not self.token:
            raise ValueError("Set LINODE_TOKEN in the environment")

    def request(self, method, path, data=None):
        request = urllib.request.Request(
            "https://api.linode.com/v4/" + path,
            data=json.dumps(data).encode() if data is not None else None,
            headers={"Authorization": "Bearer " + self.token,
                     "Content-Type": "application/json"}, method=method)
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            # Do not log bodies that might contain submitted credentials.
            raise RuntimeError(f"Linode API {method} {path}: HTTP {exc.code}") from None
        except urllib.error.URLError:
            raise RuntimeError("Linode API unreachable; check connectivity and account state before retrying") from None
