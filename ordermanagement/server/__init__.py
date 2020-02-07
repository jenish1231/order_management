from flask import Flask

from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from .auth import *
from .config import Config

app = Flask(__name__)

#load configuration
app.config.from_object(Config())

#initialize bcrypt for password hashing
bcrypt = Bcrypt(app)

jwt = JWTManager(app)
