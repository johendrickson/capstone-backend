from flask import Blueprint, abort, make_response, request, Response
from app.models.user import User
from app.db import db
from app.routes.route_utilities import validate_model
from app.helpers.geocode import geocode_location

bp = Blueprint("users_bp", __name__, url_prefix="/users")

@bp.get("")
def get_users():
    users = User.query.all()
    users_response = [user.to_dict() for user in users]
    return users_response

@bp.get("/<int:id>")
def get_user(id):
    user = validate_model(User, id)
    return user.to_dict()

@bp.post("")
def create_user():
    data = request.get_json()
    if not data or "name" not in data or "email" not in data or "location_name" not in data:
        return make_response({"details": "Name, email, and location_name are required."}, 400)

    if User.query.filter_by(email=data["email"]).first():
        return make_response({"details": "Email already exists."}, 409)

    # Geocode location_name to get lat/lon
    try:
        latitude, longitude = geocode_location(data["location_name"])
    except Exception as e:
        return make_response({"details": f"Invalid location_name: {str(e)}"}, 400)

    user = User(
        name=data["name"],
        email=data["email"],
        location_name=data["location_name"],
        latitude=latitude,
        longitude=longitude,
    )
    db.session.add(user)
    db.session.commit()

    return {"user": user.to_dict()}, 201

@bp.put("/<int:id>")
def update_user(id):
    user = validate_model(User, id)
    data = request.get_json()
    if not data:
        return make_response({"details": "Request body is empty."}, 400)

    new_email = data.get("email")
    if new_email and new_email != user.email:
        if User.query.filter_by(email=new_email).first():
            return make_response({"details": "Email already exists."}, 409)

    user.name = data.get("name", user.name)
    user.email = new_email or user.email

    # If location_name updated, geocode again
    new_location_name = data.get("location_name")
    if new_location_name and new_location_name != user.location_name:
        try:
            latitude, longitude = geocode_location(new_location_name)
        except Exception as e:
            return make_response({"details": f"Invalid location_name: {str(e)}"}, 400)

        user.location_name = new_location_name
        user.latitude = latitude
        user.longitude = longitude

    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.delete("/<int:id>")
def delete_user(id):
    user = validate_model(User, id)
    db.session.delete(user)
    db.session.commit()

    return Response(status=204, mimetype="application/json")
