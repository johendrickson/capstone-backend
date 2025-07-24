import smtplib
from email.message import EmailMessage
import os
print("EMAIL_USER:", os.environ.get("EMAIL_USER"))
print("EMAIL_PASSWORD:", os.environ.get("EMAIL_PASSWORD"))


def send_email(to_email: str, subject: str, body: str):
    """Send an email using SMTP with a Gmail account."""
    email_user = os.environ.get("EMAIL_USER")
    email_password = os.environ.get("EMAIL_PASSWORD")

    if not email_user or not email_password:
        print("Email credentials not set in environment variables.")
        return False

    msg = EmailMessage()
    msg["From"] = email_user
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(email_user, email_password)
            smtp.send_message(msg)
        print(f"Email sent to {to_email}")
        return True
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")
        return False
