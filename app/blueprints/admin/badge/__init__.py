from flask import Blueprint


badge = Blueprint("badge", __name__, url_prefix = "/badge")

from app.blueprints.admin.badge import routes