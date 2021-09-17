import sys, os
import psycopg2
import numpy as np
import infoSQL as creds
conn = ""
def openConnection():# Set up a connection to the postgres server.
    global conn
    conn = psycopg2.connect(host="localhost",
                            database="demoConectados",
                            user="postgres",
                            password="CharleiAlvSql")
#SELECT QUERY 
openConnection()
cursor = conn.cursor()
schema = "public"
table = 'users'
sql_command = "SELECT * FROM {}.{};".format(str(schema), str(table))
cursor.execute(sql_command)
records = cursor.fetchall()
for row in records:
    print(row[0]) 
cursor.close()
conn.close()

#INSERT QUERY
openConnection()
cursor = conn.cursor()
schema = "public"
table = 'users'
sql_command = "INSERT INTO {}.{}(id, nombre, apellido, mail, password)VALUES (%s, %s, %s, %s, %s);".format(str(schema), str(table))
cursor.execute(sql_command, (3,'Carlos','Alvarado','cmalvarado@ufm.edu','125O34'))
conn.commit()
cursor.close()
conn.close()