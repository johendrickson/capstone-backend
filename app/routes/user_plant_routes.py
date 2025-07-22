from flask import Blueprint, request, make_response, Response
from app.models.user_plant import UserPlant
from app.models.user import User
from app.models.plant import Plant
from app.db import db
from app.routes.route_utilities import validate_model

bp = Blueprint("user_plants_bp", __name__, url_prefix="/user_plants")

@bp.post("")
def create_user_plant():
    data = request.get_json()

    required_fields = ["user_id", "plant_id", "is_outside"]
    if not data or not all(field in data for field in required_fields):
        return make_response({"details": "user_id, plant_id, and is_outside are required."}, 400)

    user = validate_model(User, data["user_id"])
    plant = validate_model(Plant, data["plant_id"])

    user_plant = UserPlant(
        user_id=user.id,
        plant_id=plant.id,
        is_outside=data["is_outside"],
        planted_date=data.get("planted_date")  # optional
    )

    db.session.add(user_plant)
    db.session.commit()

    return {"user_plant": user_plant.to_dict()}, 201

@bp.get("")
def get_all_user_plants():
    user_plants = db.session.query(UserPlant).all()
    user_plants_response = [up.to_dict() for up in user_plants]
    return user_plants_response

@bp.get("/<int:user_plant_id>")
def get_one_user_plant(user_plant_id):
    user_plant = validate_model(UserPlant, user_plant_id)
    return {"user_plant": user_plant.to_dict()}

@bp.put("/<int:user_plant_id>")
def update_user_plant(user_plant_id):
    user_plant = validate_model(UserPlant, user_plant_id)
    data = request.get_json()

    if not data:
        return make_response({"details": "Request body is empty."}, 400)

    if "is_outside" in data:
        user_plant.is_outside = data["is_outside"]
    if "planted_date" in data:
        user_plant.planted_date = data["planted_date"]

    db.session.commit()
    return Response(status=204, mimetype="application/json")

@bp.delete("/<int:user_plant_id>")
def delete_user_plant(user_plant_id):
    user_plant = validate_model(UserPlant, user_plant_id)

    db.session.delete(user_plant)
    db.session.commit()

    return Response(status=204, mimetype="application/json")
