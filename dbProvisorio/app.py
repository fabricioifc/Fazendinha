
import sqlite3
from flask import Flask


app = Flask(__name__)

def db_connection():
    conn=None
    try:
        conn = sqlite3.connect("bancoDados.db")
    except sqlite3.error as e:
        print (e)
    return conn
