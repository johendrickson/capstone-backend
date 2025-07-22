from app.db import db
from datetime import datetime

class WateringRecord(db.Model):
    __tablename__ = "watering_records"

    id = db.Column(db.Integer, primary_key=True)
    user_plant_id = db.Column(db.Integer, db.ForeignKey("user_plants.id"), nullable=False)
    watered_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user_plant = db.relationship("UserPlant", back_populates="watering_records")

    def __init__(self, user_plant_id, watered_at=None):
        self.user_plant_id = user_plant_id
        self.watered_at = watered_at or datetime.utcnow()

    def to_dict(self):
        return {
            "id": self.id,
            "user_plant_id": self.user_plant_id,
            "watered_at": self.watered_at.isoformat()
        }
