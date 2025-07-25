import os
import requests

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

def fetch_forecast_data(lat, lon):
    api_key = os.environ.get("OPENWEATHER_API_KEY")  # fixed variable name
    if not api_key:
        raise ValueError("OPENWEATHER_API_KEY environment variable is not set")

    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=imperial&appid={api_key}"

    response = requests.get(url)
    response.raise_for_status()  # raise error if response bad
    data = response.json()

    today = data["list"][0]
    temps = [entry["main"]["temp"] for entry in data["list"][:40]]
    rain_flags = [
        entry.get("rain", {}).get("3h", 0) > 0 for entry in data["list"][:40]
    ]

    return {
        "today": {
            "temp": today["main"]["temp"],
            "min": today["main"]["temp_min"],
            "max": today["main"]["temp_max"],
            "rain": today.get("rain", {}).get("3h", 0),
            "description": today["weather"][0]["description"],
        },
        "next_5_days": {
            "temps": temps,
            "rain_flags": rain_flags,
        },
    }

def get_weather_alerts_for_user(user):
    from app.helpers.geocode import geocode_location  # imported here to avoid circular imports
    from app.models.daily_weather import DailyWeather
    from app.db import db
    from datetime import date, timedelta

    lat, lon = geocode_location(user.zip_code)
    forecast = fetch_forecast_data(lat, lon)

    today = date.today()
    yesterday = today - timedelta(days=1)

    yesterday_data = DailyWeather.query.filter_by(
    latitude=user.latitude,
    longitude=user.longitude,
    date=yesterday
    ).first()
    today_temp = forecast["today"]["temp"]
    yesterday_temp = yesterday_data.high if yesterday_data else None

    alerts = []

    if detect_heat_wave(today_temp, yesterday_temp):
        alerts.append("A heat wave is forecasted for today.")
    if detect_cold_snap(today_temp, yesterday_temp):
        alerts.append("A cold snap is expected today.")
    if detect_frost(today_temp):
        alerts.append("There is a risk of frost today.")
    if detect_dry_heat(forecast["next_5_days"]["temps"], forecast["next_5_days"]["rain_flags"]):
        alerts.append("A dry heat wave is expected over the next few days.")

    return alerts