from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from core.config import Config


db = SQLAlchemy()
login = LoginManager()
migrate = Migrate()


def create_app() -> Flask:
    app = Flask(
        import_name=__name__,
        template_folder=Config.TEMPLATE_FOLDER,
        static_folder=Config.STATIC_FOLDER
    )
    app.config.from_object(Config)

    db.init_app(app)
    login.init_app(app)
    migrate.init_app(app, db)

    @login.user_loader
    def load_user(uid: int):
        from core.models import Users
        return Users.query.get(uid)

    @app.context_processor
    def inject_globals():
        from core.constansts.privileges import Privileges
        from core import utils

        return dict(
            has_privilege=utils.has_privilege,
            is_banned=utils.is_banned,
            is_restricted=utils.is_restricted,
            check_user_status=utils.check_user_status,
            privileges_groups=utils.get_privileges_checklist,
            Privileges=Privileges
        )

    from blueprints.admin import admin
    app.register_blueprint(admin)

    from blueprints.site import site
    app.register_blueprint(site)

    return app