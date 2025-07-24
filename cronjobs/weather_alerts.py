# app/helpers/weather_alerts.py

from app import create_app
from app.models.user import User
from app.helpers.weather_api import get_weather_alerts_for_user
from app.helpers.email import send_email

app = create_app()

def run_weather_alerts_for_all_users():
    with app.app_context():
        users = User.query.all()
        for user in users:
            alerts = get_weather_alerts_for_user(user)
            if alerts:
                alert_message = "\n".join(alerts)
                subject = "Plant Pal: Weather Alert for Your Area"
                body = (
                    f"Hello {user.name},\n\n"
                    f"The following weather alerts are active for your area:\n\n"
                    f"{alert_message}\n\n"
                    "Please take appropriate action to protect your plants.\n\n"
                    "- Plant Pal"
                )
                send_email(
                    to_email=user.email,
                    subject=subject,
                    body=body
                )

if __name__ == "__main__":
    run_weather_alerts_for_all_users()
