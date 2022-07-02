import sqlite3

conn = sqlite3.connect("bancoDados.db")
cur=conn.cursor()

cur.execute("""
DROP TABLE users
""")