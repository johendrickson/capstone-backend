import os
from datetime import date, timedelta
from app.helpers.weather_api import fetch_forecast_data
from app.helpers.geocode import geocode_location
from app.models.daily_weather import DailyWeather
from app.db import db
from app.models.user import User
from app.helpers.email import send_email
from app import create_app

app = create_app()

def detect_heat_wave(today_temp, yesterday_temp):
    if today_temp is None or yesterday_temp is None:
        return False
    return (today_temp - yesterday_temp) >= 15 and today_temp > 85

def detect_cold_snap(today_temp, yesterday_temp):
    if today_temp is None or yesterday_temp is None:
        return False
    return (yesterday_temp - today_temp) >= 10 and today_temp <= 32

def detect_frost(today_temp):
    if today_temp is None:
        return False
    return today_temp <= 32

def detect_dry_heat(forecast_temps, forecast_rain):
    if not forecast_temps or not forecast_rain:
        return False

    no_rain_days = 0
    total_temp = 0

    for rain, temp in zip(forecast_rain, forecast_temps):
        if rain:
            no_rain_days = 0
            total_temp = 0
        else:
            no_rain_days += 1
            total_temp += temp

    return no_rain_days >= 3 and (total_temp / no_rain_days) >= 80

def get_weather_alerts_for_user(user):
    # Use lat/lon if available on user model, else geocode using ZIP code
    if hasattr(user, "latitude") and hasattr(user, "longitude") and user.latitude and user.longitude:
        lat, lon = user.latitude, user.longitude
    else:
        lat, lon = geocode_location(user.zip_code)

    forecast_data = fetch_forecast_data(lat, lon)

    today_temp = forecast_data["today"]["temp"]
    today_min = forecast_data["today"]["min"]
    today_max = forecast_data["today"]["max"]
    today_rain = forecast_data["today"]["rain"]
    today_description = forecast_data["today"]["description"]

    forecast_temps = forecast_data["next_5_days"]["temps"]
    forecast_rain = forecast_data["next_5_days"]["rain_flags"]

    yesterday = date.today() - timedelta(days=1)
    yesterday_weather = DailyWeather.query.filter_by(date=yesterday, latitude=lat, longitude=lon).first()
    yesterday_temp = yesterday_weather.max_temp if yesterday_weather else None

    alerts = []

    if today_temp is not None and detect_frost(today_temp):
        alerts.append("Frost expected today.")

    if yesterday_temp is not None:
        if today_temp is not None and detect_cold_snap(today_temp, yesterday_temp):
            alerts.append("Cold snap warning!")
        if today_temp is not None and detect_heat_wave(today_temp, yesterday_temp):
            alerts.append("Heat wave incoming.")

    if detect_dry_heat(forecast_temps, forecast_rain):
        alerts.append("Dry heat spell expected.")

    # Save today's weather if not already saved
    existing = DailyWeather.query.filter_by(date=date.today(), latitude=lat, longitude=lon).first()
    if not existing:
        today_weather = DailyWeather(
            date=date.today(),
            latitude=lat,
            longitude=lon,
            min_temp=today_min if today_min is not None else 0,
            max_temp=today_max if today_max is not None else 0,
            precipitation=today_rain if today_rain is not None else 0,
            did_rain=today_rain > 0 if today_rain is not None else False,
            weather_description=today_description,
        )
        db.session.add(today_weather)
        db.session.commit()

    return alerts

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
