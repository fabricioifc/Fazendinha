import sqlite3
conn = sqlite3.connect("bancoDados.db")
cur=conn.cursor()

cur.execute(""" 
INSERT INTO readings (hour_reading, id_instance_FK, number_resource_FK, value) VALUES ('2020-06-21 00:06:58', '3', '3303', '21.8') 
""")
conn.commit()
conn.close()