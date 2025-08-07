from app.db import db
from datetime import datetime

# Association table for many-to-many UserPlant <-> Tag
userplant_tags = db.Table(
    "userplant_tags",
    db.Column("user_plant_id", db.Integer, db.ForeignKey("user_plants.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True)
)

class UserPlant(db.Model):
    __tablename__ = "user_plants"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    plant_id = db.Column(db.Integer, db.ForeignKey("plants.id"), nullable=False)
    is_outdoor = db.Column(db.Boolean, nullable=False)
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

    # many-to-many tags relationship
    tags = db.relationship(
        "Tag",
        secondary=userplant_tags,
        back_populates="user_plants"
    )

    def __init__(self, user_id, plant_id, is_outdoor, planted_date=None):
        self.user_id = user_id
        self.plant_id = plant_id
        self.is_outdoor = is_outdoor
        self.planted_date = planted_date if planted_date else None

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "plant_id": self.plant_id,
            "is_outdoor": self.is_outdoor,
            "planted_date": self.planted_date.isoformat() if self.planted_date else None,
            "tags": [tag.to_dict() for tag in self.tags],
            "plant": self.plant.to_dict() if self.plant else None,
            "watering_schedule": {
                "id": self.watering_schedule.id,
                "frequency_days": self.watering_schedule.frequency_days,
                "last_watered": self.watering_schedule.last_watered.isoformat() if self.watering_schedule.last_watered else None
            } if self.watering_schedule else None,
            "watering_records": [record.to_dict() for record in self.watering_records] if self.watering_records else []
        }

