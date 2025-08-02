from flask import Blueprint, request, jsonify
from app.helpers.geocode import geocode_location
from app.helpers.weather_api import fetch_forecast_data

bp = Blueprint("weather_bp", __name__, url_prefix="/weather")

@bp.get("")
def get_weather_summary():
    zip_code = request.args.get("zip")
    if not zip_code:
        return jsonify({"error": "zip code required"}), 400

    try:
        lat, lon = geocode_location(zip_code)
        forecast = fetch_forecast_data(lat, lon)
        today = forecast["today"]

        return jsonify({
            "temp": round(today["temp"]),
            "description": today["description"],
            "zip_code": zip_code
        })

    except Exception as e:
        print(f"Weather fetch error: {e}")
        return jsonify({"error": "Weather data unavailable"}), 500
