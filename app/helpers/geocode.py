import os
import requests

def geocode_location(location: str):
    """Convert a location string to latitude and longitude using LocationIQ API."""
    api_key = os.getenv("LOCATIONIQ_API_KEY")
    if not api_key:
        raise EnvironmentError("LOCATIONIQ_API_KEY is not set")

    url = "https://us1.locationiq.com/v1/search.php"
    params = {
        "key": api_key,
        "q": location,
        "format": "json",
        "limit": 1
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()
    if not data:
        raise ValueError(f"Location not found")

    lat = float(data[0]["lat"])
    lon = float(data[0]["lon"])
    return lat, lon
