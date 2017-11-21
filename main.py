from flask import Flask, render_template, session, redirect, url_for, request, flash
import os
import utils.getty as images


app = Flask(__name__)
#Returns true if the session has necessary keys set when launching quiz
def takingQuiz():
    return set(['score', 'record', 'genre', 'difficulty', 'format']).issubset(session)
#Returns true if the user is logged in by checking for that key
def loggedIn():
    return 'user' in session


@app.route('/')
def root_route():
    print images.search("hello")[0]
    return render_template("login.html")

@app.route('/login', methods=['GET', 'POST'])
def login_logic():
    if request.method == "GET": #filters POST requests
        return redirect(url_for("root_route"))
    uname = request.form.get("username", "")
    pword = request.form.get("password", "")
    if uname == pword: #replace with login validation function
        session["user"] = uname
        return redirect(url_for("user_page"))
    else:
        flash("Wrong username or password")
        return redirect(url_for("root_route"))

@app.route('/home')
def user_page():
    if not loggedIn():
        flash("Must be logged in to view home page")
        return redirect(url_for("root_route"))
    else:
        return render_template("user.html", username=session['user'])

@app.route('/scores')
def view_high_scores():
    if not loggedIn():
        flash("Must be logged in to view your scores")
        return redirect(url_for("root_route"))
    else:
        return "High scores template"

#This is where the user selects a quiz genre
@app.route('/select')
def select_quiz():
    if not loggedIn():
        flash("Must be logged in to take a quiz")
        return redirect(url_for("root_route"))
    else:
        return render_template("select.html", username=session['user'])

#/select should redirect here, this is a functional route (no html)
#this will set up cookies for the quiz then redirect to /play
@app.route('/launch', methods=["POST"])
def begin_quiz():
    if not loggedIn():
        flash("Must be logged in to take a quiz")
        return redirect(url_for("root_route"))
    else:
        #set up cookies for quiz
        session["score"] = str(0)
        session['record'] = 0 #replace with call to DB to get high score
        session['genre'] = request.form.get("genre", "22") #geography by default
        session['difficulty'] = request.form.get("difficulty", "easy") #easy by default
        session['format'] = request.form.get("type", "multiple") #multiple choice by default
        return redirect(url_for("take_quiz"))

#Displays a question and when the user answers it redirects to /check with the answer choice ID
@app.route('/play')
def take_quiz():
    if not loggedIn():
        flash("Must be logged in to take a quiz")
        return redirect(url_for("root_route"))
    elif not takingQuiz():
        flash("You must select a quiz first")
        return redirect(url_for("user_page"))
    else:
        """
        1) get question using trivia api
        2) render the template
        """
        return "This page displays one question"

#selecting an answer to a question in /play sends you here
#if you got it right, sends to /play to answer another
@app.route('/check', methods=["POST"])
def check_answer():
    if not loggedIn():
        flash("Must be logged in to take a quiz")
        return redirect(url_for("root_route"))
    elif not takingQuiz():
        flash("You must select a quiz first")
        return redirect(url_for("user_page"))
    else:
        """
        1) check if answer is correct by testing if the answer code is divisible by 7
        2) if it is divisible by 7, then add to score and redirect to /play
        3) if it is not, then redirect to /results
        """
        return "This route should not be accessed by users"

#Getting a question wrong sends you here
@app.route('/results')
def score_report():
    if not loggedIn():
        flash("Must be logged in to view this page")
        return redirect(url_for("root_route"))
    elif not takingQuiz():
        flash("You must take a quiz to see the score")
        return redirect(url_for("user_page"))
    else:
        score = int(session.get("score", "0"))
        high = int(session.get("record", "0"))
        #render a template telling the user their score
        return "You got " + str(score) + " correct answers"

#Log out route, redirects to home page when done
@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop("user")
    return redirect(url_for("root_route"))


if __name__ == "__main__":
    app.debug = True
    app.secret_key = os.urandom(32)
    app.run()
