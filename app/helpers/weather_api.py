import requests
import os
from datetime import datetime
from app.models.daily_weather import DailyWeather

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

def fetch_forecast_data(lat, lon):
    """
    Gets current and 5-day forecast data from OpenWeather API for a location.
    Returns detailed info including today's min/max temps and precipitation.
    """
    url = "https://api.openweathermap.org/data/2.5/onecall"
    params = {
        "lat": lat,
        "lon": lon,
        "exclude": "minutely,hourly,alerts",
        "units": "imperial",
        "appid": OPENWEATHER_API_KEY
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    today_data = data["daily"][0]

    today_temp = today_data["temp"]["day"]
    today_min = today_data["temp"]["min"]
    today_max = today_data["temp"]["max"]
    today_description = today_data["weather"][0]["description"]
    today_rain = today_data.get("rain", 0)  # rain volume for today, 0 if none

    forecast_temps = [day["temp"]["day"] for day in data["daily"][:5]]
    forecast_rain = [("rain" in day) for day in data["daily"][:5]]

    return {
        "today": {
            "temp": today_temp,
            "min": today_min,
            "max": today_max,
            "description": today_description,
            "rain": today_rain
        },
        "next_5_days": {
            "temps": forecast_temps,
            "rain_flags": forecast_rain
        }
    }

def store_today_weather(user, db_session):
    """
    Fetch today's weather and store it in the DailyWeather table,
    using the user's stored latitude and longitude.
    """
    if user.latitude is None or user.longitude is None:
        raise ValueError("User does not have latitude and longitude set")

    lat, lon = user.latitude, user.longitude
    weather_data = fetch_forecast_data(lat, lon)
    today = datetime.utcnow().date()

    # Check for existing record for this date and location
    existing = DailyWeather.query.filter_by(date=today, latitude=lat, longitude=lon).first()
    if existing:
        return  # Already stored today's data

    today_data = weather_data["today"]

    new_entry = DailyWeather(
        date=today,
        latitude=lat,
        longitude=lon,
        min_temp=today_data.get("min", today_data["temp"]),
        max_temp=today_data.get("max", today_data["temp"]),
        precipitation=today_data.get("rain", 0),
        did_rain=today_data.get("rain", 0) > 0,
        weather_description=today_data.get("description", ""),
    )

    db_session.add(new_entry)
    db_session.commit()
