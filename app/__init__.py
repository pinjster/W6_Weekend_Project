from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)

login_manager = LoginManager(app)
login_manager.login_view = 'auth.signin'
login_manager.login_message = 'You must login to proceed'

from app.blueprints.main import bp as main
app.register_blueprint(main)
from app.blueprints.api import bp as api
app.register_blueprint(api)
from app.blueprints.auth import bp as auth
app.register_blueprint(auth)
from app.blueprints.fight import bp as fight
app.register_blueprint(fight)
from app.blueprints.find import bp as find
app.register_blueprint(find)
from app.blueprints.user import bp as user
app.register_blueprint(user)

from app import models