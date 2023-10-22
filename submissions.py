from db import db
from flask import redirect, render_template, request, session
from sqlalchemy import text 
from werkzeug.security import check_password_hash, generate_password_hash


def new_submission(user_id, user_text):

    try:
        sql = text("INSERT INTO submissions (user_id, text) VALUES (:user_id, :text)")
        db.session.execute(sql, {"user_id":user_id, "text":user_text})
        db.session.commit()
        return True
    except:
        return False


def fetch_ratings():

    try:
        sql = text("""SELECT submissions.id, submissions.text, ROUND(AVG(ratings.rating_value), 1) AS average_rating
                   FROM submissions LEFT JOIN ratings ON submissions.id = ratings.submission_id
                   GROUP BY submissions.id, submissions.text ORDER BY submissions.id DESC;""")
        submissions = db.session.execute(sql)
        submissions_fetch = submissions.fetchall()
        return submissions_fetch
    except:
        return None


def existing_rating(user_id, submission_id):

    try:
        sql = text("SELECT rating_value FROM ratings WHERE user_id=:user_id AND submission_id=:submission_id")
        rating = db.session.execute(sql, {"user_id":user_id, "submission_id":submission_id})
        rating_fetch = rating.fetchone()
        return rating_fetch
    except:
        return None


def add_rating(user_id, submission_id, rating_value):

    if existing_rating(user_id,submission_id):
        try:
            sql = text("DELETE FROM ratings WHERE user_id=:user_id AND submission_id=:submission_id")
            db.session.execute(sql, {"user_id":user_id, "submission_id":submission_id})
            db.session.commit()
        except:
            pass
    try:
        sql = text("INSERT INTO ratings (user_id, submission_id, rating_value) VALUES (:user_id, :submission_id, :rating_value)")
        db.session.execute(sql, {"user_id":user_id, "submission_id":submission_id, "rating_value":rating_value})
        db.session.commit()
    except:
        pass


def existing_review(user_id, submission_id):

    sql = text("SELECT review FROM reviews WHERE user_id=:user_id AND submission_id=:submission_id")
    rating = db.session.execute(sql, {"user_id":user_id, "submission_id":submission_id})
    rating_fetch = rating.fetchone()
    return rating_fetch


def add_review(user_id, submission_id, review):

    if existing_review(user_id,submission_id):
        sql = text("DELETE FROM reviews WHERE user_id=:user_id AND submission_id=:submission_id")
        db.session.execute(sql, {"user_id":user_id, "submission_id":submission_id})
        db.session.commit()

    sql = text("INSERT INTO reviews (user_id, submission_id, review) VALUES (:user_id, :submission_id, :review)")
    db.session.execute(sql, {"user_id":user_id, "submission_id":submission_id, "review":review})
    db.session.commit()


def fetch_reviews(submission_id):
        
        sql = text("""SELECT submissions.id, submissions.text, reviews.review
                   FROM submissions LEFT JOIN reviews ON submissions.id = reviews.submission_id
                   WHERE submissions.id=:submission_id""")
        review = db.session.execute(sql, {"submission_id":submission_id})
        review_fetch = review.fetchall()
        return review_fetch