from flask import Blueprint

from app.blueprints.admin.cryptocurrency import cryptocurrency

admin = Blueprint("admin", __name__, url_prefix="/admin")
admin.register_blueprint(cryptocurrency)

from app.blueprints.admin import routes