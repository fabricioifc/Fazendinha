import csv
import sqlite3
  
  
try:
  
    # Import csv and extract data
    with open('../data/datasets/object.csv', 'r') as fin:
        dr = csv.DictReader(fin)
        objectCSV = [(i['timestamp'], i['instance'], i['resource'], i['value']) for i in dr]
        print(objectCSV)
  
    # Connect to SQLite
    conn = sqlite3.connect('bancoDados.db')
    cur = conn.cursor()
  
    # Insert data into table
    cur.executemany(
        "insert into readings (hour_reading, id_instance_FK, number_resource_FK, value) VALUES (?, ?, ?, ?);", objectCSV)
  
    # Commit work and close connection
    conn.commit()
    cur.close()
  
except sqlite3.Error as error:
    print('Error occured - ', error)
  
finally:
    if conn:
        conn.close()
        print('SQLite Connection closed')