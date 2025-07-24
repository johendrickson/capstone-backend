from app import create_app
from app.models.user import User
from app.helpers.email import send_email
from app.db import db
from datetime import date

app = create_app()

def get_watering_reminders_for_user(user):
    """
    Return a list of plant names that need watering today.
    """
    reminders = []
    today = date.today()

    for plant in user.plants:
        if plant.last_watered_date is None:
            reminders.append(plant.name)
        elif (today - plant.last_watered_date).days >= plant.water_every_days:
            reminders.append(plant.name)

    return reminders

def run_watering_reminders_for_all_users():
    with app.app_context():
        users = User.query.all()
        for user in users:
            reminders = get_watering_reminders_for_user(user)
            if reminders:
                plant_list = ", ".join(reminders)
                subject = "Plant Pal: Watering Reminder 💧"
                body = (
                    f"Hello {user.name},\n\n"
                    f"Don't forget to water your plants today: {plant_list}\n\n"
                    "Keep your plants happy!\n\n"
                    "- Plant Pal"
                )
                send_email(
                    to_email=user.email,
                    subject=subject,
                    body=body
                )
