import os
from typing import Union, Tuple
import requests
from flask import make_response, Response


def geocode_location(zip_code: str):
    """Convert a zip code string to latitude and longitude using LocationIQ API."""
    api_key = os.getenv("LOCATIONIQ_API_KEY")
    if not api_key:
        raise EnvironmentError("LOCATIONIQ_API_KEY is not set")

    url = "https://us1.locationiq.com/v1/search.php"

    # Try with postalcode and countrycodes params for more accuracy
    params = {
        "key": api_key,
        "postalcode": zip_code,
        "format": "json",
        "limit": 1
    }

    response = requests.get(url, params=params, timeout=100)
    response.raise_for_status()

    data = response.json()
    # Debug: print full response to help debug location data issues
    print(f"LocationIQ response for postalcode {zip_code}: {data}")

    if not data or len(data) == 0:
        # fallback: try query param with "zip_code, USA"
        params = {
            "key": api_key,
            "q": f"{zip_code}, USA",
            "format": "json",
            "limit": 1
        }
        response = requests.get(url, params=params, timeout=100)
        response.raise_for_status()
        data = response.json()
        print(f"Fallback LocationIQ response for q='{zip_code}, USA': {data}")
        if not data or len(data) == 0:
            raise ValueError(f"Location not found for zip code: {zip_code}")

    lat = float(data[0]["lat"])
    lon = float(data[0]["lon"])
    return lat, lon

def get_coordinates_or_error(zip_code):
    try:
        lat, lon = geocode_location(zip_code)
        return (lat, lon)
    except Exception as e:
        return make_response({"details": f"Invalid zip_code: {str(e)}"}, 400)
