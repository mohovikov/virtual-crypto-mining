from flask import Blueprint

from app.blueprints.api.task import task


api = Blueprint("api", __name__, url_prefix="/api")
api.register_blueprint(task)