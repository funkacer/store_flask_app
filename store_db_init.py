import sqlite3
con = sqlite3.connect("froshims.db")
con.execute("DROP TABLE IF EXISTS registrants;")
con.execute("CREATE TABLE registrants (id INTEGER, name TEXT NOT NULL, sport TEXT NOT NULL, sex BOOL, PRIMARY KEY (id));")
con.close()
