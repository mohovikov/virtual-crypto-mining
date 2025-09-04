from flask import Blueprint


privileges = Blueprint("privileges", __name__, url_prefix = "/privileges")

from app.blueprints.admin.privileges import routes