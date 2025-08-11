from flask import Flask

from app import privileges as p
from app.helpers import check_user_status, get_privileges, get_privilege_group
from app.extensions import db, migrate, redis_client, scheduler, login_manager, bcrypt
from app.config import Config


def create_app() -> Flask:
    app = Flask(
        import_name=__name__,
        template_folder=Config.TEMPLATE_FOLDER,
        static_folder=Config.STATIC_FOLDER
    )

    @app.context_processor
    def inject_global():
        return dict(
            Privileges=p.Privileges,
            has_privilege=p.has_privilege,
            is_restricted=p.is_restricted,
            is_banned=p.is_banned,
            check_user_status=check_user_status,
            get_privileges=get_privileges,
            get_privilege_group=get_privilege_group
        )

    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)

    from app import models

    bcrypt.init_app(app)
    login_manager.init_app(app)
    redis_client.init_app(app)
    scheduler.init_app(app)
    scheduler.start()

    from app.blueprints.admin import admin
    app.register_blueprint(admin)

    from app.blueprints.site import site
    app.register_blueprint(site)

    return app