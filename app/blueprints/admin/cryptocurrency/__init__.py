from flask import Blueprint

cryptocurrency = Blueprint("cryptocurrency", __name__, url_prefix="/cryptocurrency")

from app.blueprints.admin.cryptocurrency import routes