import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from flask import Flask
from flask_cors import CORS
from .db import db, migrate

load_dotenv()

DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    "?sslmode=require"
)

print(DATABASE_URL)
print("app __init__ file read")

def create_app(config=None):
    print("app inside create_app")
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

    print("app creating engine")
    engine = create_engine(DATABASE_URL)
    print("app created engine")

    try:
        with engine.connect() as connection:
            print("Connection successful!")
    except Exception as e:
        print(f"Failed to connect: {e}\n\n\n")
        raise Exception(f"Database connection failed: {e}")

    if config:
        app.config.update(config)

    # Initialize app with SQLAlchemy db and Migrate
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models here to avoid circular imports
    print("app importing models")
    from .models.plant import Plant
    from .models.user import User
    from .models.user_plant import UserPlant
    from .models.watering_record import WateringRecord
    from .models.watering_schedule import WateringSchedule
    from .models.daily_weather import DailyWeather
    from .models.tag import Tag

    # Import and register blueprints here as well
    print("app importing blueprints/routes")
    from app.routes.user_routes import bp as users_bp
    from app.routes.user_plant_routes import bp as user_plants_bp
    from app.routes.plant_routes import bp as plants_bp
    from app.routes.tag_routes import bp as tags_bp

    print("app registering blueprints")
    app.register_blueprint(users_bp)
    app.register_blueprint(user_plants_bp)
    app.register_blueprint(plants_bp)
    app.register_blueprint(tags_bp)

    allowed_origins = [
        "http://localhost:3000",               # React dev server URL
        "https://plant-pal-frontend.onrender.com"  # Replace with your actual deployed frontend URL
    ]
    CORS(app, resources={r"/*": {"origins": allowed_origins}})

    return app
