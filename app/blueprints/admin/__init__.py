from flask import Blueprint

from app.blueprints.admin.cryptocurrency import cryptocurrency
from app.blueprints.admin.task import task

admin = Blueprint("admin", __name__, url_prefix="/admin")
admin.register_blueprint(cryptocurrency)
admin.register_blueprint(task)

from app.blueprints.admin import routes