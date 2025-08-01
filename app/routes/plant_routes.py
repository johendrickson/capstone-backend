from flask import Blueprint, request, make_response, Response
from app.models.plant import Plant
from app.db import db
from app.routes.route_utilities import validate_model
from app.helpers.gemini import generate_plant_info_from_scientific_name, suggest_scientific_name

bp = Blueprint("plants_bp", __name__, url_prefix="/plants")

@bp.get("/<int:id>")
def get_plant(id):
    plant = validate_model(Plant, id)
    return {"plant": plant.to_dict()}

@bp.get("")
def get_plants():
    query = db.select(Plant)
    plants = db.session.scalars(query).all()
    return {"plants": [plant.to_dict() for plant in plants]}

@bp.post("")
def create_plant():
    request_body = request.get_json()

    required_fields = ["scientific_name"]
    missing_fields = [field for field in required_fields if field not in request_body or not request_body[field]]

    if missing_fields:
        return make_response(
            {"details": f"Missing required field(s): {', '.join(missing_fields)}"},
            400
        )

    # Only enrich with Gemini if scientific_name is present
    if request_body.get("scientific_name"):
        gemini_data = generate_plant_info_from_scientific_name(request_body["scientific_name"])
        for key, value in gemini_data.items():
            if key not in request_body or not request_body[key]:
                request_body[key] = value

    new_plant = Plant(
        scientific_name=request_body["scientific_name"],
        common_name=request_body.get("common_name"),
        species=request_body.get("species"),
        preferred_soil_conditions=request_body.get("preferred_soil_conditions"),
        propagation_methods=request_body.get("propagation_methods"),
        edible_parts=request_body.get("edible_parts"),
        is_pet_safe=request_body.get("is_pet_safe"),
        image_url=request_body.get("image_url")
    )

    db.session.add(new_plant)
    db.session.commit()

    return {"plant": new_plant.to_dict()}, 201

@bp.get("/suggest")
def get_scientific_name_suggestions():
    partial_name = request.args.get("partial_name")

    if not partial_name:
        return make_response({"details": "Query param 'partial_name' is required."}, 400)

    suggestions = suggest_scientific_name(partial_name)
    return {"suggestions": suggestions}

@bp.put("/<int:id>")
def update_plant(id):
    plant = validate_model(Plant, id)
    request_body = request.get_json()

    if not request_body:
        return make_response({"details": "Request body is empty."}, 400)

    plant.scientific_name = request_body.get("scientific_name", plant.scientific_name)
    plant.common_name = request_body.get("common_name", plant.common_name)
    plant.species = request_body.get("species", plant.species)
    plant.preferred_soil_conditions = request_body.get("preferred_soil_conditions", plant.preferred_soil_conditions)
    plant.propagation_methods = request_body.get("propagation_methods", plant.propagation_methods)
    plant.edible_parts = request_body.get("edible_parts", plant.edible_parts)
    plant.is_pet_safe = request_body.get("is_pet_safe", plant.is_pet_safe)
    plant.image_url = request_body.get("image_url", plant.image_url)

    db.session.commit()
    return Response(status=204)

@bp.delete("/<int:id>")
def delete_plant(id):
    plant = validate_model(Plant, id)
    db.session.delete(plant)
    db.session.commit()
    return Response(status=204)
