import sqlite3
conn = sqlite3.connect("bancoDados.db")
cur=conn.cursor()



print (cur.execute(""" 
SELECT * FROM readings WHERE number_resource_FK='3303' ORDER BY hour_reading DESC LIMIT 50 
""").fetchall())
conn.commit()
conn.close()