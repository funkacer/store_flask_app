import sqlite3
con = sqlite3.connect("store.db")
con.execute("DROP TABLE IF EXISTS books;")
con.execute("CREATE TABLE books (id INTEGER, title TEXT NOT NULL, PRIMARY KEY (id));")
con.close()
