import sqlite3

conn = sqlite3.connect("bancoDados.db")
cur=conn.cursor()

cur.execute("""
CREATE TABLE ambientes (
    id integer PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    status integer NOT NULL
)
""")

cur.execute("""
CREATE TABLE resources (
    id integer PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    resource_number integer NOT NULL,
    vlini real NOT NULL,
    vlfim real NOT NULL
)
""")

cur.execute("""
CREATE TABLE instances (
    id integer PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    ambiente_id integer NOT NULL,
    instance_number integer NOT NULL,
    status integer NOT NULL,
    foreign key (ambiente_id) references ambientes (id)
)
""")

cur.execute("""
CREATE TABLE instance_resource (
    id integer PRIMARY KEY AUTOINCREMENT,
    status integer NOT NULL,
    resource_id integer NOT NULL,
    instance_id integer NOT NULL,
    normal integer NOT NULL,
    foreign key (resource_id) references resources (id)
    foreign key (instance_id) references instances (id)
)
""")

conn.commit()

cur.close()