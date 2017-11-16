from flask import Flask, render_template, session, redirect, url_for

app = Flask(__name__)

@app.route('/')
def root_route():
    return ""

@app.route('/home')
def user_page():
    return ""

if __name__ == "__main__":
    app.debug = True
    app.run()
