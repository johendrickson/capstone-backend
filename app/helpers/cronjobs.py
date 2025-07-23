from app.models.user import User
from app.helpers.weather_alerts import get_weather_alerts_for_user
from app.helpers.watering_reminders import get_watering_reminders_for_user
from helpers.email import send_email
from datetime import datetime

def run_daily_alerts():
    print(f"Running daily alerts for {datetime.now()}...")

    users = User.query.all()

    for user in users:
        weather_alerts = get_weather_alerts_for_user(user)
        watering_reminders = get_watering_reminders_for_user(user)

        if weather_alerts or watering_reminders:
            message_lines = []

            if weather_alerts:
                message_lines.append("🌡️ Weather Alerts:")
                for alert in weather_alerts:
                    message_lines.append(f"- {alert}")

            if watering_reminders:
                message_lines.append("\n💧 Watering Reminders:")
                for plant_name in watering_reminders:
                    message_lines.append(f"- {plant_name}")

            full_message = "\n".join(message_lines)

            send_email(
                to=user.email,
                subject="🌱 Your Daily PlantPal Alerts",
                body=full_message
            )
