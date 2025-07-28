from flask import Flask
from app.routes.parser_routes import parser_bp
from .limiter import limiter
import logging


def create_app():
    app= Flask(__name__)
    logging.basicConfig(level=logging.INFO)
    app.logger.setLevel(logging.INFO)
    limiter.init_app(app)
    app.register_blueprint(parser_bp)
    return app
