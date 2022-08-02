import sqlite3
conn = sqlite3.connect("bancoDados.db")
cur=conn.cursor()

id_environment = 1
print (cur.execute(""" 
SELECT * FROM environment
""".format(id_environment)).fetchall())
conn.commit()
conn.close()

