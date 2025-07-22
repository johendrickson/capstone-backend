from flask import Flask
from flask_cors import CORS
from .db import db, migrate
import os

# Import models, blueprints, and anything else needed to set up the app or database
from .models import plant, user, user_plant, watering_record, watering_schedule
from app.routes.user_routes import bp as users_bp
from app.routes.user_plant_routes import bp as user_plants_bp
from app.routes.plant_routes import bp as plants_bp
from app.routes.cronjob_routes import bp as cronjobs_bp

def create_app(config=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

    if config:
        app.config.update(config)

    # Initialize app with SQLAlchemy db and Migrate
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    app.register_blueprint(users_bp)
    app.register_blueprint(user_plants_bp)
    app.register_blueprint(plants_bp)
    app.register_blueprint(cronjobs_bp)

    CORS(app)
    return app
