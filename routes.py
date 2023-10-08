from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from app import app
from db import db, User, Submission, Rating


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
