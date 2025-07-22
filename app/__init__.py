from flask import Flask
from flask_cors import CORS
from .db import db, migrate
import os

def create_app(config=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

    if config:
        app.config.update(config)

    # Initialize app with SQLAlchemy db and Migrate
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models here to avoid circular imports
    from .models.plant import Plant
    from .models.user import User
    from .models.user_plant import UserPlant
    from .models.watering_record import WateringRecord
    from .models.watering_schedule import WateringSchedule

    # Import and register blueprints here as well
    from app.routes.user_routes import bp as users_bp
    from app.routes.user_plant_routes import bp as user_plants_bp
    from app.routes.plant_routes import bp as plants_bp
    from app.routes.cronjob_routes import bp as cronjobs_bp

    app.register_blueprint(users_bp)
    app.register_blueprint(user_plants_bp)
    app.register_blueprint(plants_bp)
    app.register_blueprint(cronjobs_bp)

    CORS(app)
    return app
