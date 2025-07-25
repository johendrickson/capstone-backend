from app import create_app
from app.models.user import User
from app.helpers.email import send_email
from cronjobs.weather_alerts import get_weather_alerts_for_user
from app.db import db

app = create_app()

with app.app_context():
    users = User.query.all()

    # for user in users:
        # alerts = get_weather_alerts_for_user(user)
        # alerts = ["This is a test alert to verify email sending."]
        # if alerts:
        #     message = "\n".join(alerts)
        #     sent = send_email(
        #         to=user.email,
        #         subject="Weather Alert for Your Plants 🌿",
        #         body=message
        #     )
        #     print(f"Email sent to {user.email}: {sent}", flush=True)


    print("Starting sending emails", flush=True)
    for user in users:
        print(f"Sending to {user.email}", flush=True)
        sent = send_email(
            to=user.email,
            subject="Weather Alert for Your Plants 🌿",
            body=message
        )
    print(f"Email sent to {user.email}: {sent}", flush=True)
print("Finished sending emails", flush=True)