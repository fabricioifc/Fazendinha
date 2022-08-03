import sqlite3
conn = sqlite3.connect("bancoDados.db")
cur=conn.cursor()

id_environment = 1
print (cur.execute(""" 
SELECT hour_reading, id_instance_FK, number_resource_FK, value, id_instance, id_environment_FK, id_environment, environment.name FROM readings, instances, environment WHERE readings.number_resource_FK = 3303 AND readings.id_instance_FK = instances.id_instance AND instances.id_environment_FK = environment.id_environment AND environment.id_environment={} ORDER BY hour_reading DESC LIMIT 1
""".format(id_environment)).fetchall())
conn.commit()
conn.close()

