from flask import Blueprint, request, make_response, Response
from app.models.watering_record import WateringRecord
from app.routes.route_utilities import validate_model
from app.db import db
from datetime import datetime

bp = Blueprint("watering_records_bp", __name__, url_prefix="/watering_records")

@bp.post("")
def create_watering_record():
    data = request.get_json()
    if not data or "user_plant_id" not in data:
        return make_response({"details": "user_plant_id is required."}, 400)

    record = WateringRecord(
        user_plant_id=data["user_plant_id"],
        watered_at=data.get("watered_at")  # optional, will default in model if not provided
    )
    db.session.add(record)
    db.session.commit()

    return {"watering_record": record.to_dict()}, 201

@bp.get("")
def get_watering_records():
    user_plant_id = request.args.get("user_plant_id")
    if not user_plant_id:
        return make_response({"details": "user_plant_id query param is required."}, 400)

    records = WateringRecord.query.filter_by(user_plant_id=user_plant_id).all()
    return {"watering_records": [r.to_dict() for r in records]}

