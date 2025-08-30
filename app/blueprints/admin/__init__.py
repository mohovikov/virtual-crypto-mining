from flask import Blueprint

from app.blueprints.admin.user import user


admin = Blueprint("admin", __name__, url_prefix = "/admin")
admin.register_blueprint(user)

from app.blueprints.admin import routes