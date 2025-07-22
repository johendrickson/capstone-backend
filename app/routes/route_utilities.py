from flask import abort, make_response
from app.db import db

def validate_model(cls, model_id):
    """
    Validate if the model with the given ID exists.
    Converts model_id to int, aborts with 400 if invalid.
    Aborts with 404 if model not found.
    Returns the model instance if found.
    """
    try:
        model_id = int(model_id)
    except ValueError:
        response = {"message": f"Invalid request: invalid {cls.__name__} id"}
        abort(make_response(response, 400))

    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        response = {"message": f"{cls.__name__} not found"}
        abort(make_response(response, 404))

    return model

def get_model_by_id(cls, model_id):
    """
    Retrieve model instance by ID using db.session.get.
    Aborts with 404 if not found.
    """
    model = db.session.get(cls, model_id)
    if model is None:
        abort(make_response({"message": f"{cls.__name__} not found"}, 404))
    return model