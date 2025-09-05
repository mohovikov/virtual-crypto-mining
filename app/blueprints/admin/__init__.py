from flask import Blueprint

from app.blueprints.admin.user import user
from app.blueprints.admin.privileges import privileges
from app.blueprints.admin.badge import badge


admin = Blueprint("admin", __name__, url_prefix = "/admin")
admin.register_blueprint(user)
admin.register_blueprint(privileges)
admin.register_blueprint(badge)

from app.blueprints.admin import routes