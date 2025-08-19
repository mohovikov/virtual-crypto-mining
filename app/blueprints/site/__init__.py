from flask import Blueprint

from app.blueprints.site.clan import clan
from app.blueprints.site.settings import settings

site = Blueprint("site", __name__, url_prefix="/")
site.register_blueprint(clan)
site.register_blueprint(settings)

from app.blueprints.site import routes