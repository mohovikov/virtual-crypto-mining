from flask import Blueprint


settings = Blueprint("settings", __name__, url_prefix="/settings")

from app.blueprints.site.settings import routes