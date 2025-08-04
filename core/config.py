import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    DEBUG = True
    SECRET_KEY = "your-super-secret-key"

    SQLALCHEMY_DATABASE_URI = "sqlite:///project.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    TEMPLATE_FOLDER = os.path.join(BASE_DIR, "templates")
    STATIC_FOLDER = os.path.join(BASE_DIR, "static")