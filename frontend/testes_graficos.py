import sqlite3
conn = sqlite3.connect("bancoDados.db")
cur=conn.cursor()

print (cur.execute(""" 
SELECT hour_reading, id_instance_FK, value, id_instance, id_environment_FK, id_environment, environment.name, environment.status FROM readings, instances, environment WHERE readings.id_instance_FK=instances.id_instance ORDER BY readings.hour_reading ASC LIMIT 1
""").fetchall())
conn.commit()
conn.close()


""" SELECT hour_reading, id_instance_FK, value, id_instance, id_environment_FK, id_environment, environment.name, environment.status FROM readings, instances, environment WHERE readings.id_instance_FK=instances.id_instance  """

"""SELECT hour_reading, id_instance_FK, value, id_instance, id_environment_FK, id_environment, environment.name, environment.status FROM readings, instances, environment WHERE readings.id_instance_FK=instances.id_instance AND instances.id_environment_FK=environment.id_environment ORDER BY readings.hour_reading ASC LIMIT 1"""