from app import create_app
from app.models.user import User
from app.helpers.email import send_email
from cronjobs.weather_alerts import get_weather_alerts_for_user
from app.db import db

app = create_app()

with app.app_context():
    users = User.query.all()

    for user in users:
        alerts = get_weather_alerts_for_user(user)
        if alerts:
            message = "\n".join(alerts)
            send_email(
                to=user.email,
                subject="Weather Alert for Your Plants 🌿",
                body=message
            )
