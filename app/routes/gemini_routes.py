from flask import Blueprint, request
from app.helpers.gemini import (
    generate_plant_info_from_scientific_name,
    suggest_scientific_name
)

bp = Blueprint("gemini_bp", __name__, url_prefix="/gemini")

@bp.route("", methods=["POST"])
def fetch_gemini_info():
    data = request.get_json()
    scientific_name = data.get("scientific_name")
    if not scientific_name:
        return {"error": "scientific_name is required"}, 400

    result = generate_plant_info_from_scientific_name(scientific_name)
    if not result:
        return {"error": "No plant information found"}, 404

    return result, 200

@bp.route("/suggestions", methods=["POST"])
def fetch_scientific_name_suggestions():
    data = request.get_json()
    partial_name = data.get("partial_name")
    if not partial_name:
        return {"error": "partial_name is required"}, 400

    result = suggest_scientific_name(partial_name)
    if not result:
        result = []

    return result, 200