from flask import Blueprint, request, make_response, Response
from app.models.watering_schedule import WateringSchedule
from app.routes.route_utilities import validate_model
from app.models.user_plant import UserPlant
from app.db import db

bp = Blueprint("watering_schedules_bp", __name__, url_prefix="/watering_schedules")

@bp.post("")
def create_watering_schedule():
    data = request.get_json()
    required_fields = ["user_plant_id", "frequency_days"]
    if not data or not all(field in data for field in required_fields):
        return make_response({"details": "user_plant_id and frequency_days are required."}, 400)

    schedule = WateringSchedule(
        user_plant_id=data["user_plant_id"],
        frequency_days=data["frequency_days"],
        last_watered=data.get("last_watered")
    )

    db.session.add(schedule)
    db.session.commit()

    return {"watering_schedule": {
        "id": schedule.id,
        "user_plant_id": schedule.user_plant_id,
        "frequency_days": schedule.frequency_days,
        "last_watered": schedule.last_watered.isoformat() if schedule.last_watered else None
    }}, 201

@bp.patch("/<int:schedule_id>")
def update_watering_schedule(schedule_id):
    schedule = validate_model(WateringSchedule, schedule_id)
    data = request.get_json()
    if not data:
        return make_response({"details": "Request body is empty."}, 400)

    if "frequency_days" in data:
        schedule.frequency_days = data["frequency_days"]
    if "last_watered" in data:
        schedule.last_watered = data["last_watered"]

    db.session.commit()
    return {"watering_schedule": schedule.to_dict()}, 200

@bp.get("/<int:schedule_id>")
def get_watering_schedule(schedule_id):
    schedule = validate_model(WateringSchedule, schedule_id)
    return {
        "watering_schedule": {
            "id": schedule.id,
            "user_plant_id": schedule.user_plant_id,
            "frequency_days": schedule.frequency_days,
            "last_watered": schedule.last_watered.isoformat() if schedule.last_watered else None
        }
    }

@bp.delete("/<int:schedule_id>")
def delete_watering_schedule(schedule_id):
    schedule = validate_model(WateringSchedule, schedule_id)

    db.session.delete(schedule)
    db.session.commit()

    return Response(status=204)

@bp.get("")
def get_all_watering_schedules():
    user_id = request.args.get("user_id")
    if not user_id:
        return make_response({"details": "user_id query parameter is required."}, 400)

    schedules = (
        db.session.query(WateringSchedule)
        .join(WateringSchedule.user_plant)
        .filter_by(UserPlant.user_id == user_id)
        .all()
    )

    return {
        "watering_schedules": [
            {
                "id": s.id,
                "user_plant_id": s.user_plant_id,
                "frequency_days": s.frequency_days,
                "last_watered": s.last_watered.isoformat() if s.last_watered else None
            }
            for s in schedules
        ]
    }
