from flask import Flask
from app.routes.parser_routes import parser_bp
from app.routes.parser_routes import auth_bp
from .limiter import limiter
import logging
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from config import Config

# Initialize extensions (no app yet)
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    # Load config
    app.config.from_object(Config)

     # CORS & logging
    CORS(app)
    logging.basicConfig(level=logging.INFO)
    app.logger.setLevel(logging.INFO)
    
    # Initialize extensions with app
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)
    
    # Create tables automatically
    with app.app_context():
        from app.models import User, ResumeLog
        db.create_all()

    
    # Register blueprints
    app.register_blueprint(parser_bp)
    app.register_blueprint(auth_bp)
    
    return app