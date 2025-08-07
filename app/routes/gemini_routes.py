from flask import Blueprint, request, jsonify
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
        return jsonify({"error": "scientific_name is required"}), 400
    result = generate_plant_info_from_scientific_name(scientific_name)
    return jsonify(result)

@bp.route("/suggestions", methods=["POST"])
def fetch_scientific_name_suggestions():
    data = request.get_json()
    partial_name = data.get("partial_name")
    if not partial_name:
        return jsonify({"error": "partial_name is required"}), 400
    result = suggest_scientific_name(partial_name)
    return jsonify(result)
