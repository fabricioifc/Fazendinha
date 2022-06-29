import sqlite3

conn = sqlite3.connect("bancoDados.db")
cur=conn.cursor()

cur.execute("""
CREATE TABLE adm (
    id integer PRIMARY KEY AUTOINCREMENT,
    email text NOT NULL,
    contact text NOT NULL,
    login text NOT NULL,
    nome text NOT NULL,
    password text NOT NULL,
    role text
)
""")