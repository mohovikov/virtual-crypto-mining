from flask import Flask

from app.extensions import db, migrate, redis_client, scheduler, login_manager, bcrypt
from app.config import Config


def create_app() -> Flask:
    app = Flask(
        import_name=__name__,
        template_folder=Config.TEMPLATE_FOLDER,
        static_folder=Config.STATIC_FOLDER
    )

    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)

    from app.models import Users

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