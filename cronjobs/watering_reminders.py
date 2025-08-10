from datetime import date
from app import create_app
from app.models.user import User
from app.helpers.email import send_email
from app.db import db

app = create_app()

def get_watering_reminders_for_user(user):
    """
    Return a list of plant names that need watering today.
    Only include plants that have a watering schedule.
    """
    reminders = []
    today = date.today()

    for user_plant in user.plants:
        schedule = user_plant.watering_schedule
        if not schedule:
            continue

        last_record = (
            user_plant.watering_records and
            max((record.watered_at for record in user_plant.watering_records), default=None)
        )
        plant_name = user_plant.plant.common_name or user_plant.plant.scientific_name

        if not last_record:
            reminders.append(plant_name)
        elif (today - last_record).days >= schedule.water_every_days:
            reminders.append(plant_name)

    return reminders

def run_watering_reminders_for_all_users():
    with app.app_context():
        users = User.query.all()

        for user in users:
            if not user.watering_reminders_enabled:
                continue

            reminders = get_watering_reminders_for_user(user)
            if reminders:
                plant_list = ", ".join(reminders)
                subject = "Watering Reminder 💧"
                body = (
                    f"Hey, there!\n\n"
                    f"Looks like these guys need watered today: {plant_list}\n\n"
                    "Don't forget to give them some sug'!"
                )
                send_email(
                    to_email=user.email,
                    subject=subject,
                    body=body
                )
