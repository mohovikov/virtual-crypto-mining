import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    DEBUG = os.environ.get("DEBUG", False) in (True, "True")
    SECRET_KEY = os.environ.get("SECRET_KEY", "")

    BABEL_DEFAULT_LOCALE = "RU"

    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://{username}:{password}@{host}:{port}/{database}'.format(
        username = os.environ.get("MYSQL_USERNAME", "root"),
        password = os.environ.get("MYSQL_PASSWORD", ""),
        host = os.environ.get("MYSQL_HOST", "localhost"),
        port = int(os.environ.get("MYSQL_PORT", "3306")),
        database=os.environ.get("MYSQL_DATABASE", "cryptomine")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REDIS_URL = "redis://localhost:6379/0"

    SCHEDULER_API_ENABLED = True

    TEMPLATE_FOLDER = os.path.join(BASE_DIR, "templates")
    STATIC_FOLDER = os.path.join(BASE_DIR, "static")
    MEDIA_FOLDER = os.path.join(BASE_DIR, "media")
    CLAN_FOLDER = os.path.join(MEDIA_FOLDER, "clan")
    USER_FOLDER = os.path.join(MEDIA_FOLDER, "user")

    SPONSOR_LIMITS = {
        "hours": 24,
        "days": 30,
        "months": 6,
        "years": 3
    }

    MAIL_SERVER = os.environ.get("MAIL_SERVER", "")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 465))
    MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL", False) in (True, "True")
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", False)in (True, "True")
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", "")