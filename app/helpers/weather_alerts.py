from app.helpers.weather_api import fetch_forecast_data
from app.helpers.geocode import geocode_location

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
    Main alert runner. Gets forecast data and returns list of alerts for a user.
    """
    # Use lat/lon if available, otherwise geocode
    if hasattr(user, "lat") and hasattr(user, "lon") and user.lat and user.lon:
        lat, lon = user.lat, user.lon
    else:
        lat, lon = geocode_location(user.zip_code)  # or user.city, etc.

    forecast_data = fetch_forecast_data(lat, lon)

    today_temp = forecast_data["today"]["temp"]
    yesterday_temp = forecast_data["yesterday"]["temp"]
    forecast_temps = forecast_data["next_5_days"]["temps"]
    forecast_rain = forecast_data["next_5_days"]["rain_flags"]

    alerts = []
    if detect_frost(today_temp):
        alerts.append("Frost expected today.")
    if detect_cold_snap(today_temp, yesterday_temp):
        alerts.append("Cold snap warning!")
    if detect_heat_wave(today_temp, yesterday_temp):
        alerts.append("Heat wave incoming.")
    if detect_dry_heat(forecast_temps, forecast_rain):
        alerts.append("Dry heat spell expected.")

    return alerts
