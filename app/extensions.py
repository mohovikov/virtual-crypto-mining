from flask_apscheduler import APScheduler
from flask_migrate import Migrate
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
migrate = Migrate()
redis_client = FlaskRedis()
scheduler = APScheduler()