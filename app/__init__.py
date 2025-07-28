from flask import Flask
from app.routes.parser_routes import parser_bp
from .limiter import limiter


def create_app():
    app= Flask(__name__)
    limiter.init_app(app)
    app.register_blueprint(parser_bp)
    return app
