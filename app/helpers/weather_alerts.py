from datetime import date, timedelta
from app.helpers.weather_api import fetch_forecast_data
from app.helpers.geocode import geocode_location
from app.models.daily_weather import DailyWeather
from app.db import db

def detect_heat_wave(today_temp, yesterday_temp):
    return (today_temp - yesterday_temp) >= 15 and today_temp > 85

def detect_cold_snap(today_temp, yesterday_temp):
    return (yesterday_temp - today_temp) >= 10 and today_temp <= 32

def detect_frost(today_temp):
    return today_temp <= 32

def detect_dry_heat(forecast_temps, forecast_rain):
    no_rain_days = 0
    total_temp = 0

    for rain, temp in zip(forecast_rain, forecast_temps):
        if rain:
            no_rain_days = 0
            total_temp = 0
        else:
            no_rain_days += 1
            total_temp += temp

    if no_rain_days >= 3 and (total_temp / no_rain_days) >= 80:
        return True
    return False

def get_weather_alerts_for_user(user):
    """
    Main alert runner. Fetches forecast data and checks for weather alerts for a user.
    Saves today's weather data to the database for tomorrow's comparison.
    Returns a list of alert messages.
    """
    # Use lat/lon if available on user model, else geocode using ZIP code
    if hasattr(user, "latitude") and hasattr(user, "longitude") and user.latitude and user.longitude:
        lat, lon = user.latitude, user.longitude
    else:
        lat, lon = geocode_location(user.zip_code)

    # Fetch today's and forecast data from API
    forecast_data = fetch_forecast_data(lat, lon)

    today_temp = forecast_data["today"]["temp"]
    today_min = forecast_data["today"]["min"]
    today_max = forecast_data["today"]["max"]
    today_rain = forecast_data["today"]["rain"]
    today_description = forecast_data["today"]["description"]

    forecast_temps = forecast_data["next_5_days"]["temps"]
    forecast_rain = forecast_data["next_5_days"]["rain_flags"]

    # Get yesterday's weather from DB for comparison
    yesterday = date.today() - timedelta(days=1)
    yesterday_weather = DailyWeather.query.filter_by(date=yesterday, latitude=lat, longitude=lon).first()
    yesterday_temp = yesterday_weather.max_temp if yesterday_weather else None

    alerts = []

    if detect_frost(today_temp):
        alerts.append("Frost expected today.")

    if yesterday_temp is not None:
        if detect_cold_snap(today_temp, yesterday_temp):
            alerts.append("Cold snap warning!")
        if detect_heat_wave(today_temp, yesterday_temp):
            alerts.append("Heat wave incoming.")

    if detect_dry_heat(forecast_temps, forecast_rain):
        alerts.append("Dry heat spell expected.")

    # Save today's weather to DB if not already saved
    existing = DailyWeather.query.filter_by(date=date.today(), latitude=lat, longitude=lon).first()
    if not existing:
        today_weather = DailyWeather(
            date=date.today(),
            latitude=lat,
            longitude=lon,
            min_temp=today_min,
            max_temp=today_max,
            precipitation=today_rain,
            did_rain=today_rain > 0,
            weather_description=today_description,
        )
        db.session.add(today_weather)
        db.session.commit()

    return alerts
