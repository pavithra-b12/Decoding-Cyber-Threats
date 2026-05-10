import smtplib
from email.message import EmailMessage
import os

SENDER_EMAIL = "pavithrab1203@gmail.com"
APP_PASSWORD = "jqgmrocnmfxvjuoe"
RECEIVER_EMAIL = "per.cyber404@gmail.com"

def send_risk_report(subject, body, attachment_path):
    try:
        msg = EmailMessage()
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL
        msg["Subject"] = subject
        msg.set_content(body)

        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, "rb") as f:
                file_data = f.read()
                file_name = os.path.basename(attachment_path)

            msg.add_attachment(
                file_data,
                maintype="application",
                subtype="octet-stream",
                filename=file_name
            )

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(msg)

        print("✅ EMAIL SENT SUCCESSFULLY")
        return "Email sent successfully"

    except Exception as e:
        print("❌ Email failed:", e)
        return f"Email failed: {e}"