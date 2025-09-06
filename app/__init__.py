import os
from flask import Flask, abort, send_from_directory

from app.services.admin import get_privileges_group_by_privileges
import app.helpers.template_helper as helper
from app import extensions as ext
from app.constants import Privileges
from app.config import Config


def create_app() -> Flask:
    app = Flask(
        import_name = __name__,
        template_folder = Config.TEMPLATE_FOLDER,
        static_folder = Config.STATIC_FOLDER
    )
    app.config.from_object(Config)

    @app.context_processor
    def inject_global():
        return dict(
            Privileges = Privileges,
            privileges_list = helper.get_privileges_list,
            has_privilege = Privileges.has_privilege,
            has_any_privilege = Privileges.has_any_privilege,
            is_restricted = Privileges.is_restricted,
            is_banned = Privileges.is_banned,
            check_account_status = Privileges.check_account_status,

            check_privileges_group = get_privileges_group_by_privileges,

            version = helper.get_version(),
            is_active = helper.is_active,
            is_active_prefix = helper.is_active_prefix
        )

    @app.route("/media/<path:filename>")
    def media(filename):
        safe_path = os.path.join(Config.MEDIA_FOLDER, filename)
        if not os.path.isfile(safe_path):
            abort(404)

        dir_name = os.path.dirname(safe_path)
        file_name = os.path.basename(safe_path)
        return send_from_directory(directory=dir_name, path=file_name)

    ext.db.init_app(app)
    ext.migrate.init_app(app, ext.db)

    from app import models

    ext.babel.init_app(app)
    ext.login_manager.init_app(app)

    ext.mail.init_app(app)
    ext.scheduler.init_app(app)
    ext.scheduler.start()

    from app import tasks
    tasks.init(app)

    from app.blueprints.admin import admin
    app.register_blueprint(admin)

    from app.blueprints.site import site
    app.register_blueprint(site)

    return app