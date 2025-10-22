from flask import Flask
from app.limiter import limiter
import logging
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
# from dotenv import load_dotenv
from config import Config
# from flask_migrate import Migrate
import os


# Initialize extensions (no app yet)
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
# migrate = Migrate()  # create Migrate instance

# load_dotenv()
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    print("Using DATABASE_URL:", os.environ.get("DATABASE_URL"))
    # Load config

    # Set secret key for Flask session
    app.secret_key = os.environ.get("JWT_SECRET_KEY") or "dev-secret-key"

    # CORS & logging
    CORS(app)
    logging.basicConfig(level=logging.INFO)
    app.logger.setLevel(logging.INFO)

    # Initialize extensions with app
    db.init_app(app)
    # migrate.init_app(app, db)  # initialize migration with app & db
    bcrypt.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)

    # Create tables automatically
    with app.app_context():
        from app.models import User, ResumeLog

        db.create_all()

    from app.routes.parser_routes import parser_bp, auth_bp, main_bp

    # Register blueprints
    app.register_blueprint(parser_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app
