#!/usr/bin/env python3
"""Run on a separate Linux machine that stays up when the app server goes down."""
import argparse
import fcntl
import json
import logging
from pathlib import Path
import subprocess
import time

from common import load_config, save_json
from health import check
from notify import send_email
from recovery import recover_server, restart_container, server_recovery_needed


def initial_state():
    return {"failures": 0, "incident": False, "restart_attempts": 0,
            "server_attempted": False, "next_action": 0, "server_allowed_at": 0,
            "pending_emails": []}


class Monitor:
    def __init__(self, config):
        self.config = config
        self.path = Path(config["state_file"])
        self.state = json.loads(self.path.read_text()) if self.path.exists() else initial_state()
        # Never silently reset damaged state: that would reset recovery budgets.
        for key, value in initial_state().items():
            if key not in self.state or type(self.state[key]) is not type(value):
                raise ValueError(f"Invalid monitor state: {key}")

    def save(self):
        save_json(self.path, self.state)

    def event(self, subject, detail):
        logging.warning("%s: %s", subject, detail)
        self.state["pending_emails"].append({"subject": subject, "body": detail})
        # Bound disk use during a long SMTP outage. Keep the latest events.
        self.state["pending_emails"] = self.state["pending_emails"][-50:]
        self.save()

    def deliver(self):
        # One digest per check prevents a backlog from delaying recovery.
        queue = self.state["pending_emails"]
        if queue:
            body = "Website: " + self.config["website_url"] + "\n\n"
            body += "\n\n".join(item["subject"] + "\n" + item["body"] for item in queue)
            if send_email(self.config, queue[-1]["subject"], body):
                self.state["pending_emails"] = []
                self.save()

    def tick(self, now=None):
        now = int(time.time()) if now is None else int(now)
        c, s = self.config, self.state
        healthy, detail = check(c["website_url"], c["expected_status"],
                                c["expected_text"], c["http_timeout"])
        logging.info("Website %s: %s", "UP" if healthy else "DOWN", detail)
        if healthy:
            had_incident = s["incident"]
            pending = s["pending_emails"]
            self.state = initial_state()
            self.state["pending_emails"] = pending
            self.state["server_allowed_at"] = s["server_allowed_at"]
            self.save()
            if had_incident:
                self.event("Website recovered", detail)
            self.deliver()
            return True

        s["failures"] += 1
        self.save()
        if s["failures"] < c["failure_threshold"]:
            self.deliver()
            return False
        if not s["incident"]:
            s["incident"] = True
            self.event("Website unavailable", detail)
        if now < s["next_action"]:
            self.deliver()
            return False

        if s["restart_attempts"] < c["max_container_restarts"]:
            # Persist intent BEFORE issuing commands. An agent crash cannot erase it.
            s["restart_attempts"] += 1
            s["next_action"] = now + c["recovery_cooldown"]
            self.save()
            self.act("Container recovery", lambda: restart_container(c))
        elif (c["enable_server_recovery"] and not s["server_attempted"]
              and now >= s["server_allowed_at"]):
            s["next_action"] = now + c["recovery_cooldown"]
            self.save()
            try:
                needed, reason = server_recovery_needed(c)
                logging.warning("Server diagnosis: %s", reason)
                if needed:
                    s["server_attempted"] = True
                    s["next_action"] = now + c["boot_grace"]
                    s["server_allowed_at"] = now + c["server_recovery_cooldown"]
                    self.save()
                    self.act("Server recovery", lambda: recover_server(c))
            except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
                logging.error("Server diagnosis failed (%s)", type(exc).__name__)
        self.deliver()
        return False

    def act(self, subject, operation):
        try:
            detail = operation()
        except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
            # Do not expose remote command output or credentials in logs/email.
            detail = f"Attempt failed ({type(exc).__name__}); inspect server and configuration"
        self.event(subject, detail)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="config.json")
    parser.add_argument("--once", action="store_true", help="One check WITH recovery enabled")
    parser.add_argument("--check-only", action="store_true", help="HTTP check only; no email, state writes, or recovery")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    config = load_config(args.config)
    if args.check_only:
        healthy, detail = check(config["website_url"], config["expected_status"],
                                config["expected_text"], config["http_timeout"])
        logging.info(detail)
        return 0 if healthy else 1
    path = Path(config["state_file"])
    path.parent.mkdir(parents=True, exist_ok=True)
    with Path(str(path) + ".lock").open("w") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            logging.error("Another monitor already owns this state file")
            return 2
        monitor = Monitor(config)
        while True:
            healthy = monitor.tick()
            if args.once:
                return 0 if healthy else 1
            time.sleep(config["check_interval"])


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        pass
