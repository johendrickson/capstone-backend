from flask import Blueprint
from app.db import db
from app.models.tag import Tag
from app.routes.route_utilities import validate_model

bp = Blueprint("tags_bp", __name__, url_prefix="/tags")

@bp.get("")
def get_tags():
    """
    Retrieve all tags.
    """
    query = db.select(Tag)
    tags = db.session.scalars(query).all()
    return {"tags": [tag.to_dict() for tag in tags]}
