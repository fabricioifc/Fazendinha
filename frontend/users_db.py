import sqlite3

conn = sqlite3.connect("bancoDados.db")
cur=conn.cursor()

cur.execute("""
CREATE TABLE adm (
    id integer PRIMARY KEY AUTOINCREMENT,
    nome text NOT NULL,
    login text NOT NULL,
    senha text NOT NULL,
    email text NOT NULL,
    contato text NOT NULL,
    habilitado integer NOT NULL
)
""")

cur.execute("""
CREATE TABLE usuario_comum (
    id integer PRIMARY KEY AUTOINCREMENT,
    nome text NOT NULL,
    login text NOT NULL,
    senha text NOT NULL,
    email text NOT NULL,
    contato text NOT NULL,
    habilitado integer NOT NULL
)
""")

cur.execute("""
CREATE TABLE visitante (
    id integer PRIMARY KEY AUTOINCREMENT,
    login text NOT NULL,
    senha text NOT NULL,
    habilitado integer NOT NULL
)
""")

cur.execute("""
CREATE TABLE user_ambiente (
    id_ambiente integer NOT NULL,
    id_usuario integer NOT NULL,
    foreign key (id_ambiente) references ambientes (id),
    foreign key (id_usuario) references usuario_comum (id)
)
""")

cur.execute("""
CREATE TABLE adm_ambiente (
    id_ambiente integer NOT NULL,
    id_adm integer NOT NULL,
    foreign key (id_ambiente) references ambientes (id),
    foreign key (id_adm) references adm (id)
)
""")
