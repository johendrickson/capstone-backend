from app.db import db
from datetime import datetime

class UserPlant(db.Model):
    __tablename__ = "user_plants"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    plant_id = db.Column(db.Integer, db.ForeignKey("plants.id"), nullable=False)
    is_outside = db.Column(db.Boolean, nullable=False)
    planted_date = db.Column(db.DateTime, nullable=True)

    # Relationships
    user = db.relationship("User", back_populates="plants")
    plant = db.relationship("Plant", back_populates="user_plants")
    watering_records = db.relationship(
        "WateringRecord",
        back_populates="user_plant",
        cascade="all, delete-orphan"
    )
    watering_schedule = db.relationship(
        "WateringSchedule",
        back_populates="user_plant",
        uselist=False
    )

    def __init__(self, user_id, plant_id, is_outside, planted_date=None):
        self.user_id = user_id
        self.plant_id = plant_id
        self.is_outside = is_outside
        self.planted_date = planted_date if planted_date else None

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "plant_id": self.plant_id,
            "is_outside": self.is_outside,
            "planted_date": self.planted_date.isoformat() if self.planted_date else None,
        }
