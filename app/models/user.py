from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import db
from app.models.user_plant import UserPlant

class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)

    plants: Mapped[list["UserPlant"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(name=data["name"], email=data["email"])
