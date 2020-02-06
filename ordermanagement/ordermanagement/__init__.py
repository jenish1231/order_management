from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from .config import Config

from order.urls import api_bp
from order.models import db


app = Flask(__name__)

#load configuration
app.config.from_object(Config())

#initialize bcrypt for password hashing
bcrypt = Bcrypt(app)

#initialize sqlalchemy
db.init_app(app)


app.register_blueprint(api_bp, url_prefix='/api')