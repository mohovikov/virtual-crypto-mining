from flask import Blueprint

from app.blueprints.site.clan import clan

site = Blueprint("site", __name__, url_prefix="/")
site.register_blueprint(clan)

from app.blueprints.site import routes