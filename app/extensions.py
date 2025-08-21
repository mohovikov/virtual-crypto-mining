from flask_apscheduler import APScheduler
from flask_babel import Babel
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mailman import Mail
from flask_migrate import Migrate
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy


babel = Babel()
bcrypt = Bcrypt()
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()
redis_client = FlaskRedis()
scheduler = APScheduler()