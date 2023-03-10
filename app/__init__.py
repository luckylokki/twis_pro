from flask_bcrypt import Bcrypt
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.config import DevelopementConfig

app = Flask(__name__)
app.config.from_object(DevelopementConfig)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.signin'

from app.views.routes.main import main
from app.views.routes.users import users

app.register_blueprint(main)
app.register_blueprint(users)
