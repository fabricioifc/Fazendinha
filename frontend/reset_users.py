import sqlite3

conn = sqlite3.connect("bancoDados.db")
cur=conn.cursor()

cur.execute("""
DROP TABLE users
""")

cur.execute("""
CREATE TABLE users (
    id integer PRIMARY KEY AUTOINCREMENT,
    email text NOT NULL,
    contact text NOT NULL,
    login text NOT NULL,
    nome text NOT NULL,
    password text NOT NULL,
    role text NOT NULL
)
""")

cur.execute("""
INSERT INTO users (email, contact, login, nome, password, role) VALUES ('admin@admin.com', '49 99999-9999', 'admin', 'admin', '123', 'ADMIN')
""")

conn.commit()
conn.close()