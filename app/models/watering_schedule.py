from app.db import db

class WateringSchedule(db.Model):
    __tablename__ = "watering_schedules"

    id = db.Column(db.Integer, primary_key=True)
    user_plant_id = db.Column(db.Integer, db.ForeignKey("user_plants.id"), nullable=False)
    frequency_days = db.Column(db.Integer, nullable=False)  # How often to water, in days
    last_watered = db.Column(db.DateTime)  # Optional: track most recent watering

    # Relationship
    user_plant = db.relationship("UserPlant", back_populates="watering_schedule")
