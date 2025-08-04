from flask import Blueprint


site = Blueprint("site", __name__, url_prefix="/")

from blueprints.site import routes