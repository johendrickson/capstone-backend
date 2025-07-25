from datetime import date
from app import create_app
from app.db import db
from app.models.user import User
from app.models.daily_weather import DailyWeather
from app.helpers.weather_api import fetch_forecast_data
from app.helpers.geocode import geocode_location

def fetch_and_store_daily_weather():
    app = create_app()

    with app.app_context():
        today = date.today()
        users = User.query.all()
        unique_locations = set()

        for user in users:
            if not user.zip_code:
                continue

            try:
                lat, lon = geocode_location(user.zip_code)
            except Exception as e:
                print(f"Failed to geocode {user.zip_code}: {e}")
                continue

            # Avoid duplicate API calls for same location
            location_key = (round(lat, 2), round(lon, 2))
            if location_key in unique_locations:
                continue
            unique_locations.add(location_key)

            # Skip if today's weather already stored
            existing = DailyWeather.query.filter_by(
                date=today,
                latitude=lat,
                longitude=lon
            ).first()

            if existing:
                print(f"Weather already stored for {lat}, {lon} on {today}")
                continue

            try:
                forecast = fetch_forecast_data(lat, lon)
                today_data = forecast["today"]

                new_weather = DailyWeather(
                    date=today,
                    latitude=lat,
                    longitude=lon,
                    min_temp=today_data["min"],
                    max_temp=today_data["max"],
                    precipitation=today_data.get("rain", 0),
                    did_rain=today_data.get("rain", 0) > 0,
                    weather_description=today_data.get("description")
                )

                db.session.add(new_weather)
                db.session.commit()
                print(f"Stored weather for {lat}, {lon} on {today}")

            except Exception as e:
                print(f"Failed to fetch/store weather for {lat}, {lon}: {e}")

if __name__ == "__main__":
    fetch_and_store_daily_weather()
