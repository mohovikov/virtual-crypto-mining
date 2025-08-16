from flask import Blueprint

clan = Blueprint("clan", __name__, url_prefix="/clan")

from app.blueprints.site.clan import routes