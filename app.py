from flask import Flask
from os import getenv
from .db import db


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = getenv("SECRET_KEY")
db.init_app(app)

from . import routes
