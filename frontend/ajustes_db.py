from datetime import datetime, timedelta
import sqlite3
conn = sqlite3.connect("bancoDados.db")
cur=conn.cursor()

conn.commit()
conn.close()






