from . import db
from datetime import datetime
import secrets

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    api_key = db.Column(db.String(50), unique=True, default=lambda: secrets.token_hex(16))

class ResumeLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    filename = db.Column(db.String(100))
    parsed_data = db.Column(db.JSON)  # Postgres JSON field
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
