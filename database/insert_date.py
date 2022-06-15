import sqlite3


conn = sqlite3.connect("bancoDados.db")
cur=conn.cursor()

cur.execute(""" 
    insert into ambientes (id, name, status) values (1, 'testes', 2)
""")