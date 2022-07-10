import sqlite3
conn = sqlite3.connect("bancoDados.db")
cur=conn.cursor()

cur.execute("""
INSERT INTO leituras VALUES ('2020-06-21 00:00:33', '3', '3316', '3.97')
""")

conn.commit()
conn.close()