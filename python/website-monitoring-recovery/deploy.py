#!/usr/bin/env python3
"""Install Docker and deploy the configured image to a fresh Ubuntu server."""
import argparse
from pathlib import Path
import shlex

from common import load_config
from recovery import run_remote


def deploy(config):
    root = Path(__file__).resolve().parent
    environment = (f"APP_IMAGE={config['image']}\nHOST_PORT={config['host_port']}\n"
                   f"CONTAINER_PORT={config['container_port']}\n")
    for name, content in (("compose.yaml", (root / "compose.yaml").read_text()),
                          (".env", environment),
                          ("health.py", (root / "health.py").read_text())):
        result = run_remote(config, "sudo -n mkdir -p /opt/website-monitoring && sudo -n tee "
                            + shlex.quote("/opt/website-monitoring/" + name) + " >/dev/null", input=content)
        if result.returncode:
            raise RuntimeError(f"Upload failed for {name}; check SSH and passwordless sudo")
    script = (root / "install-docker.sh").read_text()
    result = run_remote(config, "sudo -n bash -s", timeout=900, input=script)
    print(result.stdout)
    if result.returncode:
        print(result.stderr)
        raise RuntimeError("Remote deployment failed; inspect the output above")
    print("Deployment command completed. Run monitor.py --check-only to validate HTTP.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="config.json")
    args = parser.parse_args()
    deploy(load_config(args.config))
