"""Modules providing Flask, secret key import and db."""
from os import getenv
from flask import Flask
from db import db


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = getenv("SECRET_KEY")
db.init_app(app)

import routes
