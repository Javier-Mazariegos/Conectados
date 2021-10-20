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


#INSERT QUERY
openConnection()
cursor = conn.cursor()
schema = "public"
table = 'user_data'
sql_command = "INSERT INTO {}.{}(correo, contrasena, nombre_usuario, pais, path_foto)VALUES (%s, %s, %s, %s, %s);".format(str(schema), str(table))
cursor.execute(sql_command, ('cmalvarado@ufm.edu','125O34','cmalvarado','Guatemala', 'cmalvarado_ger.jpg'))
conn.commit()
cursor.close()
conn.close()

#SELECT QUERY 
openConnection()
cursor = conn.cursor()
schema = "public"
table = 'user_data'
sql_command = "SELECT * FROM {}.{};".format(str(schema), str(table))
cursor.execute(sql_command)
records = cursor.fetchall()
for row in records:
    print(row[0]) #id y así sucesivamente. 
cursor.close()
conn.close()