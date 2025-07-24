from app import create_app
from cronjobs.weather_alerts import run_weather_alerts_for_all_users
from cronjobs.watering_reminders import run_watering_reminders_for_all_users

app = create_app()

with app.app_context():
    run_weather_alerts_for_all_users()
    run_watering_reminders_for_all_users()
