# helpers/weather_api.py
import requests
import os

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

def fetch_forecast_data(lat, lon):
    """
    Gets current and 5-day forecast data from OpenWeather API for a location.
    """
    url = f"https://api.openweathermap.org/data/2.5/onecall"
    params = {
        "lat": lat,
        "lon": lon,
        "exclude": "minutely,hourly,alerts",
        "units": "imperial",
        "appid": OPENWEATHER_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    today_temp = data["daily"][0]["temp"]["day"]
    # yesterday’s temp is not included; simulate it for now
    yesterday_temp = today_temp - 10  # placeholder

    forecast_temps = [day["temp"]["day"] for day in data["daily"][:5]]
    forecast_rain = [("rain" in day) for day in data["daily"][:5]]

    return {
        "today": {"temp": today_temp},
        "yesterday": {"temp": yesterday_temp},
        "next_5_days": {
            "temps": forecast_temps,
            "rain_flags": forecast_rain
        }
    }

def geocode_location(zip_code):
    """
    Gets latitude and longitude from a zip code using OpenWeather's geo API.
    """
    url = f"http://api.openweathermap.org/geo/1.0/zip"
    params = {
        "zip": f"{zip_code},US",
        "appid": OPENWEATHER_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()
    return data["lat"], data["lon"]
