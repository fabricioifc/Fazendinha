import sqlite3

conn = sqlite3.connect("bancoDados.db")
cur=conn.cursor()

cur.execute("""
CREATE TABLE environment (
    id_environment integer PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    status integer NOT NULL
)
""")

cur.execute("""
CREATE TABLE resources (
    id_resource integer PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    number_resource integer NOT NULL,
    val_start real NOT NULL,
    val_end real NOT NULL
)
""")

cur.execute("""
CREATE TABLE instances (
    id_instance integer PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    id_environment_FK integer NOT NULL,
    number_instance integer NOT NULL,
    status integer NOT NULL,
    foreign key (id_environment_FK) references environment (id_environment)
)
""")

cur.execute("""
CREATE TABLE instances_resources (
    id_instance_resource integer PRIMARY KEY AUTOINCREMENT,
    status integer NOT NULL,
    id_resource_FK integer NOT NULL,
    id_instance_FK integer NOT NULL,
    normal integer NOT NULL,
    foreign key (id_resource_FK) references resources (id_resource)
    foreign key (id_instance_FK) references instances (id_instance)
)
""")

cur.execute("""
CREATE TABLE readings (
    id_reading integer PRIMARY KEY AUTOINCREMENT,
    hour_reading text NOT NULL,
    id_instance_FK integer NOT NULL,
    number_resource_FK integer NOT NULL,
    value real NOT NULL,
    foreign key (id_instance_FK) references instances (id_instance),
    foreign key (number_resource_FK) references resources (number_resource)
)
""")

conn.commit()

cur.close()