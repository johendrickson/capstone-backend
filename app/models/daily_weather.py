from app.db import db
from datetime import date

class DailyWeather(db.Model):
    __tablename__ = "daily_weather"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, index=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    min_temp = db.Column(db.Float, nullable=False)
    max_temp = db.Column(db.Float, nullable=False)
    precipitation = db.Column(db.Float, nullable=True)  # mm or inches
    did_rain = db.Column(db.Boolean, nullable=False, default=False)
    weather_description = db.Column(db.String(100), nullable=True)  # e.g. "Clear", "Rain", "Clouds"

    def __init__(self, date, latitude, longitude, min_temp, max_temp, precipitation=None, did_rain=False, weather_description=None):
        self.date = date
        self.latitude = latitude
        self.longitude = longitude
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.precipitation = precipitation
        self.did_rain = did_rain
        self.weather_description = weather_description

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date.isoformat(),
            "latitude": self.latitude,
            "longitude": self.longitude,
            "min_temp": self.min_temp,
            "max_temp": self.max_temp,
            "precipitation": self.precipitation,
            "did_rain": self.did_rain,
            "weather_description": self.weather_description,
        }
