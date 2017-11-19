from flask import Flask, render_template, session, redirect, url_for, request, flash

app = Flask(__name__)

@app.route('/')
def root_route():
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
    return render_template("user.html")

if __name__ == "__main__":
    app.debug = True
    app.secret_key = "just you, me, and the rest of the world"
    app.run()
