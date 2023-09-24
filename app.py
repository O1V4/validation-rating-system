from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)
app.secret_key = getenv("SECRET_KEY")


@app.route("/")
def index():
    submissions = Submission.query.all()

    for submission in submissions:
        if submission.ratings:
            submission.average_rating = round(sum([rating.rating_value for rating in submission.ratings]) / len(submission.ratings), 2)
        else:
            submission.average_rating = None

    return render_template("index.html", submissions=submissions)

@app.route('/newuser')
def newuser():
    return render_template('newuser.html')

@app.route('/userexists')
def userexists():
    return render_template('userexists.html')

@app.route('/usersuccess')
def usersuccess():
    return render_template('usersuccess.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()

    if user:
        return redirect('/userexists')
    else:
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/usersuccess')

@app.route("/failed")
def failed():
    return render_template('failed.html')

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        session["username"] = username
        return redirect("/")
    else:
        return redirect("/failed")
    
@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")


@app.route("/submit_text", methods=["GET", "POST"])
def submit_text():
    if "username" not in session:
        return redirect("/")
    
    if request.method == "POST":
        text = request.form["text"]
        user_id = User.query.filter_by(username=session["username"]).first().id
        new_submission = Submission(user_id=user_id, text=text)
        db.session.add(new_submission)
        db.session.commit()
        return redirect("/")
    
    return render_template("submit_text.html")

@app.route("/rate/<int:submission_id>", methods=["POST"])
def rate(submission_id):
    if "username" not in session:
        return redirect("/login")
    
    rating = request.form["rating"]
    user_id = User.query.filter_by(username=session["username"]).first().id
    
    existing_rating = Rating.query.filter_by(user_id=user_id, submission_id=submission_id).first()
    if existing_rating:
        existing_rating.rating_value = rating
    else:
        new_rating = Rating(user_id=user_id, submission_id=submission_id, rating_value=rating)
        db.session.add(new_rating)
    db.session.commit()
    return redirect("/")

@app.route("/view_submissions")
def view_submissions():
    submissions = Submission.query.all()
    return render_template("view_submissions.html", submissions=submissions)



class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(230), nullable=False)

class Submission(db.Model):
    __tablename__ = 'submissions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    ratings = db.relationship('Rating', backref='submission', lazy=True)

class Rating(db.Model):
    __tablename__ = 'ratings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    submission_id = db.Column(db.Integer, db.ForeignKey('submissions.id'), nullable=False)
    rating_value = db.Column(db.Integer, nullable=False)