"""SSH container repair and gated Linode boot/reboot operations."""
import ipaddress
import shlex
import subprocess
from urllib.parse import urlsplit

from common import Linode


def ssh_command(config):
    return ["ssh", "-i", config["ssh_key"], "-o", "BatchMode=yes",
            "-o", "StrictHostKeyChecking=yes", "-o", "IdentitiesOnly=yes",
            "-o", "UserKnownHostsFile=" + config["ssh_known_hosts"],
            "-o", "ConnectTimeout=10", "-o", "ServerAliveInterval=10",
            "-o", "ServerAliveCountMax=2", config["ssh_user"] + "@" + config["ssh_host"]]


def run_remote(config, command, timeout=90, **kwargs):
    return subprocess.run(ssh_command(config) + [command], text=True,
                          capture_output=True, timeout=timeout, **kwargs)


def restart_container(config):
    result = run_remote(config,
        "sudo -n systemctl start docker && cd /opt/website-monitoring && "
        "sudo -n docker compose up -d && sudo -n docker compose restart app")
    if result.returncode:
        raise RuntimeError(f"Remote container recovery failed (SSH exit {result.returncode})")
    return "Container recovery command completed"


def server_recovery_needed(config):
    url = urlsplit(config["website_url"])
    # Check the same path locally to avoid rebooting for a public routing problem.
    local_url = f"http://127.0.0.1:{config['host_port']}" + (url.path or "/")
    if url.query:
        local_url += "?" + url.query
    command = shlex.join(["python3", "/opt/website-monitoring/health.py", local_url,
                          "--status", str(config["expected_status"]), "--text",
                          config["expected_text"], "--timeout", str(config["http_timeout"])])
    try:
        result = run_remote(config, command, timeout=config["http_timeout"] + 30)
    except subprocess.TimeoutExpired:
        return True, "Server diagnosis timed out"
    if result.returncode == 0:
        return False, "Application responds locally; investigate public networking or TLS"
    if result.returncode == 1:
        return True, "Application also fails the local HTTP check"
    # SSH configuration/authentication errors are not evidence of a failed server.
    network_errors = ("connection timed out", "connection refused", "no route to host", "network is unreachable")
    if result.returncode == 255 and any(s in result.stderr.lower() for s in network_errors):
        return True, "Server unreachable over SSH"
    return False, "Unable to diagnose host; check SSH access and installed health.py"


def recover_server(config):
    client = Linode()
    path = f"linode/instances/{config['linode_id']}"
    instance = client.request("GET", path)
    # Reboot only the exact instance being monitored. Use its public IPv4 in config.
    host = str(ipaddress.ip_address(config["ssh_host"]))
    if host not in instance["ipv4"]:
        raise ValueError("ssh_host does not belong to linode_id; refusing server recovery")
    status = instance["status"]
    if status not in ("running", "offline"):
        return f"Linode is {status}; no power operation submitted"
    action = "boot" if status == "offline" else "reboot"
    client.request("POST", path + "/" + action, {})
    return f"Linode {action} requested"
