from flask import Blueprint, abort, make_response, request, Response
from app.models.plant import Plant
from app.db import db
from app.routes.route_utilities import validate_model

bp = Blueprint("plants_bp", __name__, url_prefix="/plants")

@bp.get("/<int:id>")
def get_plant(id):
    plant = validate_model(Plant, id)
    return {"plant": plant.to_dict()}

@bp.get("")
def get_plants():
    query = db.select(Plant)
    plants = db.session.scalars(query).all()
    plants_response = [plant.to_dict() for plant in plants]
    return {"plants": plants_response}

@bp.post("")
def create_plant():
    request_body = request.get_json()

    required_fields = ["common_name", "scientific_name"]
    if not request_body or any(field not in request_body for field in required_fields):
        return make_response({"details": "Missing required fields"}, 400)

    new_plant = Plant(
        common_name=request_body["common_name"],
        scientific_name=request_body["scientific_name"],
        species=request_body.get("species"),
        preferred_soil_conditions=request_body.get("preferred_soil_conditions"),
        propagation_methods=request_body.get("propagation_methods"),
        edible_parts=request_body.get("edible_parts"),
        is_plant_safe=request_body.get("is_plant_safe"),
    )

    db.session.add(new_plant)
    db.session.commit()

    return {"plant": new_plant.to_dict()}, 201

@bp.put("/<int:id>")
def update_plant(id):
    plant = validate_model(Plant, id)
    request_body = request.get_json()

    if not request_body:
        return make_response({"details": "Request body is empty."}, 400)

    # Update all fields if provided, else keep existing values
    plant.common_name = request_body.get("common_name", plant.common_name)
    plant.scientific_name = request_body.get("scientific_name", plant.scientific_name)
    plant.species = request_body.get("species", plant.species)
    plant.preferred_soil_conditions = request_body.get("preferred_soil_conditions", plant.preferred_soil_conditions)
    plant.propagation_methods = request_body.get("propagation_methods", plant.propagation_methods)
    plant.edible_parts = request_body.get("edible_parts", plant.edible_parts)
    plant.is_plant_safe = request_body.get("is_plant_safe", plant.is_plant_safe)

    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.delete("/<int:id>")
def delete_plant(id):
    plant = validate_model(Plant, id)

    db.session.delete(plant)
    db.session.commit()

    return Response(status=204, mimetype="application/json")
