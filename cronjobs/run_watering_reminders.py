from app import create_app
from app.models.user import User
from app.helpers.email import send_email
from app.db import db
from cronjobs.watering_reminders import get_watering_reminders_for_user

app = create_app()

with app.app_context():
    users = User.query.all()

    for user in users:
        if not user.watering_reminders_enabled:
            continue

        reminders = get_watering_reminders_for_user(user)

        if reminders:
            plant_list = ", ".join(reminders)
            body = f"Don't forget to water your plants today: {plant_list}"
            send_email(
                to_email=user.email,
                subject="Watering Reminder 💧",
                body=body
            )
