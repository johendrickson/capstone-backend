from app import create_app
from app.models.user import User
from app.helpers.email import send_email
from cronjobs.weather_alerts import get_weather_alerts_for_user
from app.db import db

print("creating app context")

app = create_app()
print("created app context")

with app.app_context():
    print("getting users from database")
    users = User.query.all()

    print("Starting sending emails", flush=True)
    for user in users:
        print(f"Sending to {user.email}", flush=True)

        # Use test alert here for now:
        alerts = ["This is a test alert to verify email sending."]
        message = "\n".join(alerts)

        sent = send_email(
            to_email=user.email,
            subject="Weather Alert for Your Plants 🌿",
            body=message
        )
        print(f"Email sent to {user.email}: {sent}", flush=True)

    print("Finished sending emails", flush=True)
