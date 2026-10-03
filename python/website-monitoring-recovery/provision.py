#!/usr/bin/env python3
"""Create one Ubuntu Linode and a cloud firewall. Run explicitly to incur costs."""
import argparse
import getpass
import ipaddress
import json
from pathlib import Path
import time

from common import Linode, save_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--label", default="website-monitoring-app")
    parser.add_argument("--region", required=True, help="Linode region ID")
    parser.add_argument("--type", default="g6-standard-1", help="Linode plan ID (2 GiB default for app + MongoDB)")
    parser.add_argument("--ssh-public-key", required=True)
    parser.add_argument("--admin-cidr", required=True, help="Monitor/admin public IPv4 CIDR; e.g. 203.0.113.10/32")
    parser.add_argument("--web-port", type=int, default=80)
    parser.add_argument("--output", default="deployment.json")
    args = parser.parse_args()
    network = ipaddress.ip_network(args.admin_cidr, strict=False)
    if network.version != 4 or network.prefixlen == 0:
        parser.error("Use a restricted IPv4 admin CIDR, not 0.0.0.0/0")
    if not 1 <= args.web_port <= 65535 or args.web_port == 22:
        parser.error("web-port must be between 1 and 65535 and different from SSH port 22")
    public_key = Path(args.ssh_public_key).expanduser().read_text().strip()
    if not public_key.startswith(("ssh-ed25519 ", "ssh-rsa ", "ecdsa-sha2-")):
        parser.error("Expected an OpenSSH public key (not a private key)")
    output = Path(args.output)
    client = Linode()
    if output.exists():
        deployment = json.loads(output.read_text())
        if deployment["label"] != args.label:
            parser.error("Existing deployment label differs; use the original settings")
        print(f"Resuming existing deployment: Linode {deployment['id']}")
    else:
        # Duplicate labels must not accidentally create another paid instance.
        page = 1
        while True:
            instances = client.request("GET", f"linode/instances?page={page}")
            if any(item["label"] == args.label for item in instances["data"]):
                parser.error("A Linode with this label exists; inspect it instead of creating another")
            if page >= instances["pages"]:
                break
            page += 1
        password = getpass.getpass("Initial root password (Linode image requirement): ")
        if len(password) < 12:
            parser.error("Use a root password of at least 12 characters")
        instance = client.request("POST", "linode/instances", {
            "label": args.label, "region": args.region, "type": args.type,
            "image": "linode/ubuntu24.04", "root_pass": password,
            "interface_generation": "legacy_config", "firewall_id": -1,
            "authorized_keys": [public_key], "booted": False,
            "tags": ["website-monitoring"]})
        deployment = {"id": instance["id"], "label": args.label,
                      "ipv4": instance["ipv4"], "firewall_id": None}
        save_json(output, deployment)
        print(f"Created Linode {instance['id']}; saved {output}")
    if not deployment["firewall_id"]:
        firewall = client.request("POST", "networking/firewalls", {
            "label": args.label + "-fw",
            "rules": {
                "inbound_policy": "DROP", "outbound_policy": "ACCEPT",
                "inbound": [
                    {"label": "ssh", "action": "ACCEPT", "protocol": "TCP", "ports": "22",
                     "addresses": {"ipv4": [str(network)]}},
                    {"label": "web", "action": "ACCEPT", "protocol": "TCP", "ports": str(args.web_port),
                     "addresses": {"ipv4": ["0.0.0.0/0"], "ipv6": ["::/0"]}}],
                "outbound": []}, "devices": {"linodes": [deployment["id"]]}})
        deployment["firewall_id"] = firewall["id"]
        save_json(output, deployment)
    deadline = time.monotonic() + 600
    boot_requested = False
    while time.monotonic() < deadline:
        instance = client.request("GET", f"linode/instances/{deployment['id']}")
        if instance["status"] == "running":
            print(f"Ready: Linode ID {instance['id']}, IPv4 {', '.join(instance['ipv4'])}")
            print("Set ssh_host, website_url, and linode_id in config.json; then run deploy.py.")
            return
        if instance["status"] == "offline" and not boot_requested:
            # Attach the firewall before exposing a booted server to the network.
            client.request("POST", f"linode/instances/{deployment['id']}/boot", {})
            boot_requested = True
        time.sleep(10)
    raise TimeoutError("Linode not running within 10 minutes; inspect Cloud Manager before retrying")


if __name__ == "__main__":
    main()
