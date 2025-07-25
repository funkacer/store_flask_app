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

# pro pythonanywhere:
DB = "mysite/store.db"
# pro localhost:
DB = "store.db"

@app.route("/")
def index():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    cur = con.execute("SELECT * from books")
    books = cur.fetchall()
    con.close()
    return render_template("books.html", name=session.get("name"), pwd=os.getcwd(), books=books)

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

