from flask import Blueprint, request, make_response
from app.helpers.geocode import get_coordinates_or_error

bp = Blueprint("geocode_bp", __name__, url_prefix="/geocode")

@bp.get("")
def geocode_by_zip():
    zip_code = request.args.get("zip_code")
    if not zip_code:
        return make_response({"details": "Missing zip_code"}, 400)

    result = get_coordinates_or_error(zip_code)

    if isinstance(result, tuple):
        lat, lon = result
        return {"lat": lat, "lon": lon}
    else:
        return result  # it's already a make_response with 400
