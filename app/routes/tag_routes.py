from flask import Blueprint, request, make_response
from app.db import db
from app.models.tag import Tag
from app.routes.route_utilities import validate_model

bp = Blueprint("tags_bp", __name__, url_prefix="/tags")


@bp.get("")
def get_tags():
    """
    GET /tags
    Returns a list of all tags.
    """
    tags = db.session.query(Tag).all()
    return make_response({"tags": [tag.to_dict() for tag in tags]}, 200)

@bp.post("")
def create_tag():
    """
    POST /tags
    Creates a new tag.
    Expects JSON body: { "name": "Low light" }
    """
    data = request.get_json()

    if not data or "name" not in data:
        return make_response({"details": "Tag name is required."}, 400)

    # Check for duplicate tag name
    existing = db.session.query(Tag).filter_by(name=data["name"]).first()
    if existing:
        return make_response({"details": f"Tag '{data['name']}' already exists."}, 400)

    new_tag = Tag(name=data["name"])
    db.session.add(new_tag)
    db.session.commit()

    return make_response({"tag": new_tag.to_dict()}, 201)

@bp.delete("/<int:tag_id>")
def delete_tag(tag_id):
    """
    DELETE /tags/<tag_id>
    Deletes the tag by ID.
    """
    tag = validate_model(Tag, tag_id)

    db.session.delete(tag)
    db.session.commit()

    return make_response({"details": f"Tag '{tag.name}' deleted."}, 200)
