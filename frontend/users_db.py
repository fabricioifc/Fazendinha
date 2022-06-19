import sqlite3

conn = sqlite3.connect("bancoDados.db")
cur=conn.cursor()

cur.execute("""
CREATE USER admin;
grant * on 
""")

cur.execute("""
CREATE USER visitante;
grant select on ambientes, resources, instances, instance_resource to visitante
""")