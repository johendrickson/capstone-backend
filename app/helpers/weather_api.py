import requests
import os
from datetime import datetime
from app.models.daily_weather import DailyWeather

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_coordinates(zip_code):
    """
    Gets latitude and longitude from a ZIP code using OpenWeather's geo API.
    """
    url = "http://api.openweathermap.org/geo/1.0/zip"
    params = {
        "zip": f"{zip_code},US",
        "appid": OPENWEATHER_API_KEY
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    if "lat" not in data or "lon" not in data:
        raise ValueError(f"Could not geocode ZIP code: {zip_code}")

    return data["lat"], data["lon"]

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
    Fetches today's weather and stores it in the DailyWeather table.
    Avoids duplicate entries for the same date and location.
    """
    lat, lon = get_coordinates(user.zip_code)
    weather_data = fetch_forecast_data(lat, lon)
    today = datetime.utcnow().date()

    # Check if entry already exists for today and location
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
