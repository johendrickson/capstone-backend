from app import create_app
from app.models.user import User
from app.helpers.email import send_email
from cronjobs.watering_reminders import get_watering_reminders_for_user
from app.db import db

app = create_app()

with app.app_context():
    users = User.query.all()

    for user in users:
        reminders = get_watering_reminders_for_user(user)
        if reminders:
            plant_list = ", ".join(reminders)
            send_email(
                to_email=user.email,
                subject="Watering Reminder 💧",
                body=f"Don't forget to water your plants today: {plant_list}"
            )
