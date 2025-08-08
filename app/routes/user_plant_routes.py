from flask import Blueprint, request, make_response, Response
from app.models.user_plant import UserPlant
from app.models.user import User
from app.models.plant import Plant
from app.models.tag import Tag
from app.db import db
from app.routes.route_utilities import validate_model

bp = Blueprint("user_plants_bp", __name__, url_prefix="/user_plants")

@bp.post("")
def create_user_plant():
    data = request.get_json()

    required_fields = ["user_id", "is_outdoor"]
    if not data or not all(field in data for field in required_fields):
        return make_response({"details": "user_id and is_outdoor are required."}, 400)

    new_plant = Plant(
        scientific_name=data["scientific_name"],
        common_name=data.get("common_name"),
        species=data.get("species"),
        preferred_soil_conditions=data.get("preferred_soil_conditions"),
        propagation_methods=data.get("propagation_methods"),
        edible_parts=data.get("edible_parts"),
        is_pet_safe=data.get("is_pet_safe"),
        image_url=data.get("image_url")
    )

    db.session.add(new_plant)
    db.session.commit()

    user = validate_model(User, data["user_id"])

    user_plant = UserPlant(
        user_id=user.id,
        plant_id=new_plant.id,
        is_outdoor=data["is_outdoor"],
        planted_date=data.get("planted_date")
    )

    tag_ids = data.get("tag_ids", [])
    if tag_ids:
        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
        user_plant.tags = tags

    db.session.add(user_plant)
    db.session.commit()

    return {"user_plant": user_plant.to_dict()}, 201

@bp.get("/all/<int:user_id>")
def get_all_user_plants(user_id):
    user_id = request.args.get("user_id")

    if user_id:
        user_plants = db.session.query(UserPlant).filter_by(user_id=user_id).all()
    else:
        user_plants = db.session.query(UserPlant).all()

    user_plants_response = [up.to_dict() for up in user_plants]
    return {"user_plants": user_plants_response}

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

    if "is_outdoor" in data:
        user_plant.is_outdoor = data["is_outdoor"]
    if "planted_date" in data:
        user_plant.planted_date = data["planted_date"]

    # Update tags if provided
    if "tag_ids" in data:
        tag_ids = data["tag_ids"]
        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
        user_plant.tags = tags

    # Update associated Plant fields
    plant = user_plant.plant

    if "scientific_name" in data:
        plant.scientific_name = data["scientific_name"]
    if "common_name" in data:
        plant.common_name = data["common_name"]
    if "species" in data:
        plant.species = data["species"]
    if "preferred_soil_conditions" in data:
        plant.preferred_soil_conditions = data["preferred_soil_conditions"]
    if "propagation_methods" in data:
        plant.propagation_methods = data["propagation_methods"]
    if "edible_parts" in data:
        plant.edible_parts = data["edible_parts"]
    if "is_pet_safe" in data:
        plant.is_pet_safe = data["is_pet_safe"]
    if "image_url" in data:
        plant.image_url = data["image_url"]

    db.session.commit()
    return Response(status=204, mimetype="application/json")

@bp.delete("/<int:user_plant_id>")
def delete_user_plant(user_plant_id):
    user_plant = validate_model(UserPlant, user_plant_id)

    db.session.delete(user_plant)
    db.session.commit()

    return Response(status=204, mimetype="application/json")
