from flask import Blueprint

task = Blueprint("task", __name__, url_prefix="/task")

from app.blueprints.admin.task import routes