"""
VISIL Notifier

Sends drift reports via email using SMTP.
"""

import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class VISILNotifier:
    def __init__(self, smtp_host, smtp_port, sender_email, sender_password):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password

    def send_email(self, recipient, subject, content):
        msg = MIMEMultipart()
        msg["From"] = self.sender_email
        msg["To"] = recipient
        msg["Subject"] = subject

        msg.attach(MIMEText(content, "plain"))

        try:
            server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
            server.quit()
            return True
        except Exception as e:
            print(f"[VISIL NOTIFIER ERROR]: {e}")
            return False

    def send_drift_report(self, recipient, report):
        content = json.dumps(report, indent=2)

        return self.send_email(
            recipient=recipient,
            subject="VISIL Drift Report",
            content=content
        )
