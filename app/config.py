import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "")

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///db.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REDIS_URL = "redis://localhost:6379/0"

    SCHEDULER_API_ENABLED = True

    TEMPLATE_FOLDER = os.path.join(BASE_DIR, "templates")
    STATIC_FOLDER = os.path.join(BASE_DIR, "static")
    MEDIA_FOLDER = os.path.join(BASE_DIR, "media")

    SPONSOR_LIMITS = {
        "hours": 24,
        "days": 30,
        "months": 3,
        "years": 1
    }