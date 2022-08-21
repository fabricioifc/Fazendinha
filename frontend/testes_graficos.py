from datetime import datetime
from datetime import timedelta
import sqlite3
conn = sqlite3.connect("bancoDados.db")
cur=conn.cursor()


""" last_reading - transdutor 3 (id_3) - horta 1 (id_2) """

env = cur.execute("""
SELECT id_environment FROM environment WHERE status = 1
""").fetchall()
id_env = 5
qtd_readings = 5
break_time = 5
average_temp=0
temp = []

chartDate = datetime.now().replace(microsecond=0, second=0) + timedelta(minutes= - (break_time * qtd_readings))
print (chartDate)
for env in env: 
    reads = cur.execute("""
    SELECT hour_reading value, environment.name FROM readings, instances, environment WHERE number_resource_FK=3303 AND readings.id_instance_FK=instances.id_instance AND instances.id_environment_FK=environment.id_environment AND environment.id_environment={} 
    ORDER BY hour_reading DESC LIMIT {}
    """.format(env[0], id_env)).fetchall()
    if reads:
        reads.reverse()
        x = 1
        for read in reads:
            hour_read = datetime.strptime(read[0], '%Y-%m-%d %H:%M:%S')
            while x<qtd_readings:
                if (hour_read >= chartDate and hour_read < (chartDate + timedelta(minutes= +break_time))):
                    """ adicionar esse horario no campo e colocar o valor dessa leitura na média que posteriormente sera colocada numa lista para então ele ser posto no gráfico """
                    print (chartDate)

                    x+=1
                    average_temp+=read[1]
                    break
                
                else:
                    """ adicionar mais 5 minutos no chartDate e adicionar um valor None na lista, ele dira que não há leituras de temperatura nesses 5 minutos """
                    chartDate = chartDate + timedelta(minutes= +break_time)

                    print (chartDate + timedelta(minutes= +break_time))
                    if average_temp:
                        temp.append()
                    temp.append(None)
                    average_temp=0
                    x+=1

        
        

    else:
        pass
        """ print (env[0]," não possui leituras") """
conn.commit()
conn.close()

