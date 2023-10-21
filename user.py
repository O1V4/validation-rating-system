from db import db
from flask import redirect, render_template, request, session
from sqlalchemy import text 
from werkzeug.security import check_password_hash, generate_password_hash


def create_user(username: str, password: str):

    password = generate_password_hash(password, method='sha256')
    sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
    db.session.execute(sql, {"username":username, "password":password})
    db.session.commit()


def username_already_exists(username: str):

    sql = text("SELECT username FROM users WHERE username=:username")
    name = db.session.execute(sql, {"username": username})
    name_fetch = name.fetchone()
    if name_fetch:
        return True
    else:
        False


def login_db(username: str, password: str):

    sql = text("SELECT id, password FROM users WHERE username=:username")
    user = db.session.execute(sql, {"username":username})
    user_fetch = user.fetchone()
    if user_fetch and check_password_hash(user_fetch[1], password):        
        return user_fetch[0]
    else:
        return None
