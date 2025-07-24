import requests
import os
from datetime import datetime, timedelta
from app.models.daily_weather import DailyWeather

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

def fetch_forecast_data(lat, lon):
    """
    Fetches 5-day weather forecast in 3-hour intervals from OpenWeather free API.
    Processes data to extract today's min/max temps, rain, and next 5 days daily temps and rain flags.
    """
    url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        "lat": lat,
        "lon": lon,
        "units": "imperial",
        "appid": OPENWEATHER_API_KEY
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    forecast_list = data.get("list", [])

    today = datetime.utcnow().date()

    # Group temps and rain flags by date
    daily_temps = {}
    daily_rain = {}

    for forecast in forecast_list:
        dt_txt = forecast["dt_txt"]  # e.g., '2025-07-24 15:00:00'
        dt = datetime.strptime(dt_txt, "%Y-%m-%d %H:%M:%S")
        date_key = dt.date()

        temp = forecast["main"]["temp"]
        rain = forecast.get("rain", {}).get("3h", 0)

        daily_temps.setdefault(date_key, []).append(temp)
        if rain > 0:
            daily_rain[date_key] = True
        else:
            # Set False only if not previously set True
            daily_rain.setdefault(date_key, False)

    # Today's data
    today_temps = daily_temps.get(today, [])
    today_min = min(today_temps) if today_temps else None
    today_max = max(today_temps) if today_temps else None
    today_avg = sum(today_temps) / len(today_temps) if today_temps else None
    today_rain = daily_rain.get(today, False)

    # Description approximation: use first forecast description for today if exists
    today_description = ""
    for forecast in forecast_list:
        dt = datetime.strptime(forecast["dt_txt"], "%Y-%m-%d %H:%M:%S")
        if dt.date() == today:
            today_description = forecast["weather"][0]["description"]
            break

    # Next 5 days data starting tomorrow
    next_5_days = []
    next_5_rain = []
    for i in range(1, 6):
        day = today + timedelta(days=i)
        temps = daily_temps.get(day, [])
        avg_temp = sum(temps) / len(temps) if temps else None
        next_5_days.append(avg_temp)
        next_5_rain.append(daily_rain.get(day, False))

    return {
        "today": {
            "temp": today_avg,
            "min": today_min,
            "max": today_max,
            "description": today_description,
            "rain": today_rain
        },
        "next_5_days": {
            "temps": next_5_days,
            "rain_flags": next_5_rain
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

    existing = DailyWeather.query.filter_by(date=today, latitude=lat, longitude=lon).first()
    if existing:
        return  # Already stored today's data

    today_data = weather_data["today"]

    new_entry = DailyWeather(
        date=today,
        latitude=lat,
        longitude=lon,
        min_temp=today_data.get("min"),
        max_temp=today_data.get("max"),
        precipitation=1 if today_data.get("rain") else 0,
        did_rain=today_data.get("rain"),
        weather_description=today_data.get("description", ""),
    )

    db_session.add(new_entry)
    db_session.commit()
