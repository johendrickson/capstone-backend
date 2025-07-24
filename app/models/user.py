from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import db
from app.models.user_plant import UserPlant

class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    zip_code: Mapped[str] = mapped_column(nullable=False)  # required zip code as string
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    plants: Mapped[list["UserPlant"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    def __init__(self, name: str, email: str, zip_code: str, latitude: float = None, longitude: float = None):
        self.name = name
        self.email = email
        self.zip_code = zip_code
        self.latitude = latitude
        self.longitude = longitude

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "zip_code": self.zip_code,
            "latitude": self.latitude,
            "longitude": self.longitude,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            email=data["email"],
            zip_code=data["zip_code"],
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
        )
