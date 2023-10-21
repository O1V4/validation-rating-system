from app import app
from flask import redirect, render_template, request, session, flash
from user import create_user, username_already_exists, login_db
from submissions import new_submission, fetch_ratings, add_rating


@app.route("/")
def index():
    
    submissions = fetch_ratings()
    return render_template("index.html", submissions=submissions)


@app.route('/register', methods=["GET", "POST"])
def register():

    if request.method == "GET":
        return render_template("register.html")
    
    if request.method == "POST":
        username = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']

        if username_already_exists(username):
            flash("Käyttäjänimi on jo olemassa, valitse toinen!")
            return render_template("register.html")

        if len(username) < 4 or len(username) > 20:
            flash("Käyttäjänimen pitää olla pituudeltaan 4-20 merkkiä!")
            return render_template("register.html")

        if len(password1) < 8:
            flash("Salasanan pitää olla vähintään 8 merkkiä pitkä!")
            return render_template("register.html")
        
        if password1 != password2:
            flash("Salasanat eivät täsmänneet!")
            return render_template("register.html")
        
        try:
            create_user(username, password1)
            return redirect('/usersuccess')
        except:
            flash("Käyttäjän luonti ei onnistunut, yritä uudelleen!")
            return render_template("register.html")


@app.route('/usersuccess')
def usersuccess():

    return render_template('usersuccess.html')


@app.route("/login",methods=["POST", "GET"])
def login():

    if request.method == "GET":
        return render_template("index.html", submissions="HUOM")

    if request.method == "POST": 
        username = request.form["username"]
        password = request.form["password"]

        check_id = login_db(username, password)
        if check_id:
            session["userid"] = check_id
            session["username"] = username
            return redirect("/")
        else:
            flash("Käyttäjänimi tai salasana on väärin, yritä uudelleen!")
            return render_template("index.html", submissions="HUOM")
        

@app.route("/logout")
def logout():

    del session["userid"]
    del session["username"]
    return redirect("/")


@app.route("/submit_text", methods=["GET", "POST"])
def submit_text():

    if "username" not in session:
        return redirect("/")
    
    if request.method == "GET":
        return render_template("submit_text.html")

    if request.method == "POST":
        user_text = request.form["text"]
        user_id = session["userid"]

        if len(user_text.strip()) < 2:
            flash("Tekstin pitää olla ainakin 2 merkkiä pitkä!")
            return render_template("submit_text.html")

        operation = new_submission(user_id, user_text)
        if operation:
            return redirect("/")
        else:
            flash("Jokin meni pieleen, yritä uudelleen!")
            return render_template("submit_text.html")
        

@app.route("/rate/<int:submission_id>", methods=["POST"])
def rate(submission_id):
    if "username" not in session:
        return redirect("/login")

    rating = request.form["rating"]
    user_id = session["userid"]

    add_rating(user_id, submission_id, rating)

    return redirect("/")
