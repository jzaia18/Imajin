from flask import Flask, render_template, session, redirect, url_for, request, flash
import utils.userOperations as users
import utils.trivia as trivia
import random
import os


app = Flask(__name__)

#Returns true if the session has necessary keys set when launching quiz
def takingQuiz():
    return set(['score', 'record', 'genre', 'difficulty', 'format']).issubset(session)

#Returns true if the user is logged in by checking for that key
def loggedIn():
    return 'user' in session

#Given a correct answer and a list of incorrect answers, will return a dictionary
#of answer-code pairs. The key will be the text of the answer, and value will be its code
#Correct answer will be divisible by 7, the rest will not
def generateAnswers(correct, incorrect):
    answers = {}
    answers[correct] = 7 * random.randint(0, 100 / 7)
    start = 1
    end = 6
    for answer in incorrect:
        answers[answer] = 3 * random.randint(start, end) #inclusive of both ends
        start += 7
        end += 7
    return answers

def randomizeAnswers(answers):
    ansList = []
    for key in sorted(answers):
        ansList.append([key, answers[key]])
    return ansList
    

#Will replace this with a call to trivia.py
def code2Subject(code):
    return trivia.codes[str(code)]


@app.route('/')
def root_route():
    return render_template("login.html")

@app.route('/user/login', methods=['GET', 'POST'])
def login_logic():
    if request.method == "GET": #filters POST requests
        return redirect(url_for("root_route"))
    uname = request.form.get("username", "")
    pword = request.form.get("password", "")
    if users.authUser(uname, pword):
        session["user"] = uname
        return redirect(url_for("user_page"))
    else:
        flash("Wrong username or password")
        return redirect(url_for("root_route"))

@app.route('/user/new', methods=['POST'])
def join_logic():
    if not ('username' in request.form):
        flash("You must enter a username to create an account")
        return redirect(url_for("root_route"))
    elif not ('password' in request.form) or len(request.form["password"]) == 0:
        flash("You must enter a password to create an account")
        return redirect(url_for("root_route"))
    elif not ('password2' in request.form):
        flash("You must confirm your password to create an account")
        return redirect(url_for("root_route"))
    else:
        uname = request.form["username"]
        pword = request.form["password"]
        confirm = request.form["password2"]
        if users.exists(uname):
            flash("This username is taken")
            return redirect(url_for("root_route"))
        elif pword != confirm:
            flash("The passwords must match")
            return redirect(url_for("root_route"))
        else:
            users.addUser(uname, pword)
            flash("Sucessfully created the account %s, you may now login" % uname)
            return redirect(url_for("root_route"))
    return redirect(url_for("root_route")) #this should never happen

@app.route('/user/home')
def user_page():
    if not loggedIn():
        flash("Must be logged in to view home page")
        return redirect(url_for("root_route"))
    else:
        return render_template("user.html", username=session['user'])

@app.route('/user/scores')
def view_high_scores():
    if not loggedIn():
        flash("Must be logged in to view your scores")
        return redirect(url_for("root_route"))
    else:
        return render_template("records.html", username=session['user'], scores=users.getHighscores(session['user']))

#This is where the user selects a quiz genre
@app.route('/quiz/select')
def select_quiz():
    if not loggedIn():
        flash("Must be logged in to take a quiz")
        return redirect(url_for("root_route"))
    else:
        return render_template("select.html", username=session['user'], subjects=trivia.subjects)

#/select should redirect here, this is a functional route (no html)
#this will set up cookies for the quiz then redirect to /play
@app.route('/quiz/launch', methods=["POST"])
def begin_quiz():
    if not loggedIn():
        flash("Must be logged in to take a quiz")
        return redirect(url_for("root_route"))
    else:
        #set up cookies for quiz
        session["score"] = 0
        session['genre'] = request.form.get("genre", "22") #geography by default
        session['record'] = users.getHighscore(session['user'], code2Subject(int(session['genre'])))
        session['difficulty'] = request.form.get("difficulty", "easy") #easy by default
        session['format'] = request.form.get("type", "multiple") #multiple choice by default
        return redirect(url_for("take_quiz"))

#Displays a question and when the user answers it redirects to /check with the answer choice ID
@app.route('/quiz/play')
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
        question_data = trivia.gimmie(session["genre"], session["difficulty"], session["format"])
        if len(question_data) == 0: #error getting question
            flash("You have answered all the questions in this category")
            return redirect(url_for("score_report"))
        q = question_data[0]
        a = randomizeAnswers(generateAnswers(question_data[1], question_data[2:]))
        return render_template("question.html", question=q, answers=a)

#selecting an answer to a question in /play sends you here
#if you got it right, sends to /play to answer another
@app.route('/quiz/check', methods=["POST"])
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
        answer_code = int(request.form.get("answer", "3"))
        print answer_code
        if answer_code % 7 == 0: #correct
            session["score"] = int(session["score"]) + 1
            flash("You answered the last question correctly")
            return redirect(url_for("take_quiz"))
        else: #wrong
            flash("You ended your streak by not selecting the correct answer to the last question.")
            return redirect(url_for("score_report"))

#Getting a question wrong sends you here
@app.route('/quiz/results')
def score_report():
    if not loggedIn():
        flash("Must be logged in to view this page")
        return redirect(url_for("root_route"))
    elif not takingQuiz():
        flash("You must take a quiz to see the score")
        return redirect(url_for("user_page"))
    else:
        who = session["user"]
        score = int(session["score"])
        record = int(session["record"])
        subject = code2Subject(int(session["genre"]))
        if score > record:
            users.addHighscore(who, subject, score)
        #render a template telling the user their score
        return render_template("score.html", username=who, subject=subject, record=record, score=score, quote="Inspirational quote")

#Log out route, redirects to home page when done
@app.route('/user/logout')
def logout():
    if 'user' in session:
        session.pop("user")
    return redirect(url_for("root_route"))


if __name__ == "__main__":
    app.debug = True
    app.secret_key = os.urandom(32)
    app.run()
