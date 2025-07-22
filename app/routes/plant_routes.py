from flask import Blueprint

bp = Blueprint('plants', __name__)

# You can leave it empty for now, or add a simple test route:
@bp.route('/')
def index():
    return "User routes placeholder"
