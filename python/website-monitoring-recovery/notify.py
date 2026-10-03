"""TLS email alerts. SMTP failure never stops application recovery."""
import argparse
from email.message import EmailMessage
import logging
import os
import smtplib
import ssl

from common import load_config


def send_email(config, subject, body):
    try:
        message = EmailMessage()
        message["Subject"] = "[Website Monitor] " + subject
        message["From"] = config["email_from"]
        message["To"] = ", ".join(config["email_to"])
        message.set_content(body)
        context = ssl.create_default_context()
        if config["smtp_security"] == "ssl":
            client = smtplib.SMTP_SSL(config["smtp_host"], config["smtp_port"], timeout=15, context=context)
        else:
            client = smtplib.SMTP(config["smtp_host"], config["smtp_port"], timeout=15)
        with client:
            if config["smtp_security"] == "starttls":
                client.starttls(context=context)
            username = os.environ.get("SMTP_USERNAME")
            if username:
                client.login(username, os.environ.get("SMTP_PASSWORD", ""))
            refused = client.send_message(message)
            if refused:
                logging.error("Some email recipients were rejected")
                return False
        return True
    except (OSError, smtplib.SMTPException, ValueError) as exc:
        logging.error("Email delivery failed (%s); will retry", type(exc).__name__)
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send a test monitoring email")
    parser.add_argument("--config", default="config.json")
    args = parser.parse_args()
    raise SystemExit(0 if send_email(load_config(args.config), "Test alert", "Email notifications are configured.") else 1)
