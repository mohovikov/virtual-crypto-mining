import os
from flask import Flask, abort, send_from_directory

from app import helpers, services
from app.constants import Privileges
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
            Privileges=Privileges,
            has_privilege=Privileges.has_privilege,
            has_any_privilege=Privileges.has_any_privilege,
            is_restricted=Privileges.is_restricted,
            is_banned=Privileges.is_banned,
            is_locked=Privileges.is_locked,
            check_user_status=helpers.check_user_status,
            get_privileges=helpers.get_privileges,
            get_clan_link=helpers.get_clan_link,
            get_privilege_group=services.get_privilege_group
        )

    @app.route("/media/<path:filename>")
    def media(filename):
        safe_path = os.path.join(Config.MEDIA_FOLDER, filename)
        if not os.path.isfile(safe_path):
            abort(404)

        dir_name = os.path.dirname(safe_path)
        file_name = os.path.basename(safe_path)
        return send_from_directory(directory=dir_name, path=file_name)

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