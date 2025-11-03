import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///test.db")
    print("Inside Config, DATABASE_URL =", SQLALCHEMY_DATABASE_URI)
    # "sqlite:///db.sqlite3"   fallback for local dev

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    # JWT
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "super-secret-key")
    # set on Render
    # Other optional configs
    DEBUG = os.environ.get("DEBUG", "False") == "True"
