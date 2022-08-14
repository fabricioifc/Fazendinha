import sqlite3
conn = sqlite3.connect("bancoDados.db")
cur=conn.cursor()



cur.execute("""
CREATE TABLE resources (
    id_resource integer PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    number_resource integer NOT NULL,
    val_start real NOT NULL,
    val_end real NOT NULL
)
""")

conn.commit()
conn.close()






