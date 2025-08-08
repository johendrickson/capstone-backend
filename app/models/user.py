from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import db
from app.models.user_plant import UserPlant

class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    zip_code: Mapped[str] = mapped_column(nullable=False)
    garden_name: Mapped[str] = mapped_column(nullable=False, default="Your Garden")

    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    watering_reminders_enabled: Mapped[Optional[bool]] = mapped_column(nullable=True, default=True)
    weather_alerts_enabled: Mapped[Optional[bool]] = mapped_column(nullable=True, default=True)

    plants: Mapped[list["UserPlant"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __init__(
        self,
        name: str,
        email: str,
        zip_code: str,
        garden_name: Optional[str] = "Your Garden",
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        watering_reminders_enabled: bool = True,
        weather_alerts_enabled: bool = True
    ):
        self.name = name
        self.email = email
        self.zip_code = zip_code
        self.garden_name = garden_name or "Your Garden"
        self.latitude = latitude
        self.longitude = longitude
        self.watering_reminders_enabled = watering_reminders_enabled
        self.weather_alerts_enabled = weather_alerts_enabled

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "zip_code": self.zip_code,
            "garden_name": self.garden_name,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "watering_reminders_enabled": self.watering_reminders_enabled,
            "weather_alerts_enabled": self.weather_alerts_enabled,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            email=data["email"],
            zip_code=data["zip_code"],
            garden_name=data.get("garden_name", "Your Garden"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            watering_reminders_enabled=data.get("watering_reminders_enabled", True),
            weather_alerts_enabled=data.get("weather_alerts_enabled", True)
        )
