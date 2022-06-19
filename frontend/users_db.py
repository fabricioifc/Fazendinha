import sqlite3

conn = sqlite3.connect("bancoDados.db")
cur=conn.cursor()

cur.execute("""
CREATE user admin WITH PASSWORD '1234';
GRANT ALL PRIVILEGES ON bancoDados.db TO admin;
""")

cur.execute("""
CREATE user visitante;
grant select on ambientes, resources, instances, instance_resource to visitante
""")

