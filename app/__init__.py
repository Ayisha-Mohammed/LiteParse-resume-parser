from flask import Flask
from app.routes.parser_routes import parser_bp

def create_app():
    app= Flask(__name__)
    app.register_blueprint(parser_bp)
    return app
    
  