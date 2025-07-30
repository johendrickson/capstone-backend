"""
This code is part of a Flask application that provides geocoding functionality
using the LocationIQ API. It includes functions to convert a zip code into
latitude and longitude coordinates, and to handle errors gracefully by returning
appropriate HTTP responses.
"""

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
    params = {
        "key": api_key,
        "q": zip_code,
        "format": "json",
        "limit": 1
    }

    response = requests.get(url, params=params, timeout=100)
    response.raise_for_status()

    data = response.json()
    if not data or len(data) == 0:
        raise ValueError(f"Location not found for zip code: {zip_code}")

    lat = float(data[0]["lat"])
    lon = float(data[0]["lon"])
    return lat, lon


def get_coordinates_or_error(zip_code) -> Union[Tuple[float, float], Response]:
    """
    Wrapper that attempts to get coordinates from a zip code.
    Returns a (lat, lon) tuple on success,
    or a Flask Response (error JSON + status 400) on failure.
    """
    try:
        return geocode_location(zip_code)
    except Exception as e:
        return make_response({"details": f"Invalid zip_code: {str(e)}"}, 400)
