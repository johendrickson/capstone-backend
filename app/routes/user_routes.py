from flask import Blueprint, request, jsonify, abort
from app.models.user import User
from app.db import db
from app.routes.route_utilities import validate_model  # helper to check if model instance exists

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])


@bp.route('/<int:id>', methods=['GET'])
def get_user(id):
    user = validate_model(User, id)
    return jsonify(user.to_dict())


@bp.route('', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'name' not in data or 'email' not in data:
        abort(400, 'Name and email are required.')

    # Check if email already exists?
    if User.query.filter_by(email=data['email']).first():
        abort(409, 'Email already exists.')

    user = User(name=data['name'], email=data['email'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


@bp.route('/<int:id>', methods=['PUT'])
def update_user(id):
    user = validate_model(User, id)
    data = request.get_json()
    if not data:
        abort(400, 'Request body is empty.')

    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    db.session.commit()
    return jsonify(user.to_dict())


@bp.route('/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = validate_model(User, id)
    db.session.delete(user)
    db.session.commit()
    return '', 204
