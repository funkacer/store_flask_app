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
    cur = con.execute("SELECT * FROM books")
    books = cur.fetchall()
    con.close()
    return render_template("books.html", books=books)

@app.route("/cart", methods=["GET", "POST"])
def cart():
    if "cart" not in session:
        session["cart"] = []
    if request.method == "POST":
        book_id = request.form.get("id")
        if book_id:
            session["cart"].append(book_id)
        return redirect("/cart")
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    cur = con.execute(f"SELECT * FROM books WHERE id IN ({','.join(session['cart'])})")
    #cur = con.execute(f"SELECT * FROM books WHERE id IN (?)", session["cart"])
    books = cur.fetchall()
    con.close()
    return render_template("cart.html", books=books)

