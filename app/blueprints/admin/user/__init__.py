from flask import Blueprint


user = Blueprint("user", __name__, url_prefix = "/user")

from app.blueprints.admin.user import routes