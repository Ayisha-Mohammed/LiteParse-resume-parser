import os


class Config:
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///db.sqlite3"  # fallback for local dev
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # JWT
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "super-secret-key")
    # set on Render
    # Other optional configs
    DEBUG = os.environ.get("DEBUG", "False") == "True"
