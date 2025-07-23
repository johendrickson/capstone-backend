from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import db
from app.models.user_plant import UserPlant

class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    location_name: Mapped[str] = mapped_column(nullable=False)  # Required location name
    latitude: Mapped[float] = mapped_column(nullable=True)
    longitude: Mapped[float] = mapped_column(nullable=True)

    plants: Mapped[list["UserPlant"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    def __init__(self, name: str, email: str, location_name: str, latitude: float = None, longitude: float = None):
        self.name = name
        self.email = email
        self.location_name = location_name
        self.latitude = latitude
        self.longitude = longitude

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "location_name": self.location_name,
            "latitude": self.latitude,
            "longitude": self.longitude,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            email=data["email"],
            location_name=data["location_name"],  # required
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
        )