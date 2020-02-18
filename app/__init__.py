from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

public_key = app.config['RECAPTCHA_PUBLIC_KEY']

login = LoginManager(app)

login.login_view = 'login'
login.login_message = "Пожалуйста, войдите, чтобы открыть эту страницу."

moment = Moment(app)

mail = Mail(app)

from app import views, models, errors, admin_views
