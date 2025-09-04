from flask import Blueprint

from app.blueprints.admin.user import user
from app.blueprints.admin.privileges import privileges


admin = Blueprint("admin", __name__, url_prefix = "/admin")
admin.register_blueprint(user)
admin.register_blueprint(privileges)

from app.blueprints.admin import routes