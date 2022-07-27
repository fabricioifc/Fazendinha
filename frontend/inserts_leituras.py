import sqlite3
conn = sqlite3.connect("bancoDados.db")
cur=conn.cursor()

cur.execute(""" 
INSERT INTO readings (hour_reading, id_instance_FK, number_resource_FK, value) VALUES ('2020-06-21 00:16:37', '3', '3303', '21.7') 
""")
conn.commit()
conn.close()