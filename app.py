# mkdir froshims_flask_app
# cd froshims_flask_app
# cp ../my_flask_app/requirements.txt .
# . ../../bin/activate (. _Git/_test/bin/activate)
# pip install -r requirements.txt
# touch app.py
# mkdir templates
# touch layout.html index.html
# flask run

from flask import Flask, render_template, redirect, request, session
from flask_session import Session
import sqlite3
import os

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

DB = "store.db"

@app.route("/")
def index():
    return render_template("index.html", name=session.get("name"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["name"] = request.form.get("name")
        return redirect("/")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/")
def index():
    return render_template("index.html", sports=SPORTS, pwd=os.getcwd())

@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    if not name:
        return render_template("error.html", message="Missing name")
    sport = request.form.get("sport")
    if not sport:
        return render_template("error.html", message="Missing sport")
    if sport not in SPORTS:
        return render_template("error.html", message="Invalid sport")
    sex = next(filter(lambda x: SEX[x]==request.form.get("sex"), SEX.keys()), None)
    con = sqlite3.connect(DB)
    with con:
        con.execute("INSERT INTO registrants (name, sport, sex) VALUES (?, ?, ?)", [name, sport, sex])
    con.close()
    return render_template("success.html")

@app.route("/registrants")
def registrants():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    cur = con.execute("SELECT * from registrants")
    registrants = cur.fetchall()
    con.close()
    return render_template("registrants.html", registrants=registrants, SEX=SEX)
