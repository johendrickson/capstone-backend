from flask import Blueprint, make_response, request, Response
from app.models.user import User
from app.db import db
from app.routes.route_utilities import validate_model
from app.helpers.geocode import get_coordinates_or_error

bp = Blueprint("users_bp", __name__, url_prefix="/users")

@bp.get("")
def get_users():
    users = User.query.all()
    users_response = [user.to_dict() for user in users]
    return {"users": users_response}

@bp.get("/<int:id>")
def get_user(id):
    user = validate_model(User, id)
    return {"user": user.to_dict()}

@bp.post("")
def create_user():
    data = request.get_json()
    if not data or "name" not in data or "email" not in data or "zip_code" not in data:
        return make_response({"details": "Name, email, and zip_code are required."}, 400)

    if User.query.filter_by(email=data["email"]).first():
        return make_response({"details": "Email already exists."}, 409)

    coords = get_coordinates_or_error(data["zip_code"])
    if isinstance(coords, Response):
        return coords

    latitude, longitude = coords

    user = User(
        name=data.get("name"),
        email=data.get("email"),
        zip_code=data.get("zip_code"),
        latitude=latitude,
        longitude=longitude,
        garden_name=data.get("garden_name", "Your Garden")  # <-- NEW
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

    new_zip = data.get("zip_code")
    if new_zip and new_zip != user.zip_code:
        coords = get_coordinates_or_error(new_zip)
        if isinstance(coords, Response):
            return coords
        user.latitude, user.longitude = coords
        user.zip_code = new_zip

    if "garden_name" in data:
        user.garden_name = data["garden_name"]

    db.session.commit()

    return {"user": user.to_dict()}, 200

@bp.delete("/<int:id>")
def delete_user(id):
    user = validate_model(User, id)
    db.session.delete(user)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.post("/login")
def login_user():
    data = request.get_json()
    if not data or "email" not in data:
        return make_response({"details": "Email is required."}, 400)

    user = User.query.filter_by(email=data["email"]).first()
    if not user:
        return make_response({"details": "Invalid email or user not found."}, 401)

    return {"user": user.to_dict()}, 200
