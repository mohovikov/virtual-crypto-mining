from flask_babel import Babel
from flask_login import LoginManager
from flask_mailman import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


babel = Babel()
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()