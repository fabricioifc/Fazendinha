from datetime import datetime
from datetime import timedelta
import sqlite3
conn = sqlite3.connect("bancoDados.db")
cur=conn.cursor()

""" last_reading - transdutor 3 (id_3) - horta 1 (id_2) """

env = cur.execute("""
SELECT id_environment FROM environment WHERE status = 1
""").fetchall()
y = 5
now =  timedelta(days = 5)
print (now)

for env in env:
    x = cur.execute("""
    SELECT hour_reading value, environment.name FROM readings, instances, environment WHERE number_resource_FK=3303 AND readings.id_instance_FK=instances.id_instance AND instances.id_environment_FK=environment.id_environment AND environment.id_environment={} 
    AND hour_reading >=
    ORDER BY hour_reading DESC LIMIT {}
    """.format(env[0], y)).fetchall()
    x.reverse()
    if x:
        print (x)
        """ now = datetime.now()
        print (now.strftime("%F %T")) """

        

    else:
        print (env[0]," não possui leituras")
conn.commit()
conn.close()






