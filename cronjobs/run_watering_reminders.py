from app import create_app
from app.models.user import User
from app.helpers.email import send_email
from cronjobs.watering_reminders import get_watering_reminders_for_user
from app.db import db

app = create_app()

with app.app_context():
    users = User.query.all()
    print(f"Found {len(users)} users.", flush=True)

    for user in users:
        print(f"Checking reminders for user: {user.email}", flush=True)
        reminders = get_watering_reminders_for_user(user)

        # FORCE AN EMAIL, even if empty
        if reminders:
            plant_list = ", ".join(reminders)
            body = f"Don't forget to water your plants today: {plant_list}"
        else:
            print(f"No reminders found for {user.email} — sending test email anyway.", flush=True)
            body = "This is a test email from GitHub Actions. No plants to water today, but you're getting this so we know email works 💧"

        try:
            send_email(
                to_email=user.email,
                subject="Watering Reminder 💧",
                body=body
            )
            print(f"Email sent to {user.email}", flush=True)
        except Exception as e:
            print(f"Failed to send email to {user.email}: {e}", flush=True)
