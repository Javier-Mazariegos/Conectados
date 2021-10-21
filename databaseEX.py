import sys, os
import psycopg2
conn = ""
def openConnection():# Set up a connection to the postgres server.
    global conn
    conn = psycopg2.connect(host="localhost",
                            database="demoConectados",
                            user="postgres",
                            password="CharleiAlvSql")


#INSERT QUERY
#openConnection()
#cursor = conn.cursor()
#schema = "public"
#table = 'user_data'
#sql_command = "INSERT INTO {}.{}(correo, contrasena, nombre_usuario, pais, path_foto)VALUES (%s, %s, %s, %s, %s);".format(str(schema), str(table))
#cursor.execute(sql_command, ('cmalvarado@ufm.edu','125O34','cmalvarado','Guatemala', 'cmalvarado_ger.jpg'))
#conn.commit()
#cursor.close()
#conn.close()

#SELECT QUERY 
#openConnection()
#cursor = conn.cursor()
#schema = "public"
#table = 'user_data'
#sql_command = "SELECT * FROM {}.{};".format(str(schema), str(table))
#cursor.execute(sql_command)
#records = cursor.fetchall()
#for row in records:
#    print(row[0]) #id y así sucesivamente. 
#cursor.close()
#conn.close()

#Query de info de usuario: SELECT para validar en registro y traer el id si ya existe en caso de login
openConnection()
cursor = conn.cursor()
schema = "public"
table = 'user_data'
correo = "cmalvarado@ufm.edu"
#sql_command = "SELECT id FROM {}.{} WHERE {}.{}.correo = %s;".format(str(schema), str(table), str(schema), str(table))
sql_command = "SELECT id FROM public.user_data WHERE public.user_data.correo = %s and public.user_data.contrasena = %s;"
cursor.execute(sql_command, (correo, '125O34'))
records = cursor.fetchall()
for row in records:
    print(row[0]) #id y así sucesivamente. 
cursor.close()
conn.close()

#--------------------------
print('----------------')
#Query de info de usuario: SELECT por login si ya se verifico que existe y quiero ir a cuenta
openConnection()
cursor = conn.cursor()
correo = "cmalvarado@ufm.edu"
sql_command = "SELECT id, correo, nombre_usuario, pais, path_foto FROM public.user_data WHERE  public.user_data.correo = %s and public.user_data.contrasena = %s;"
cursor.execute(sql_command, (correo, '125O34'))
records = cursor.fetchall()
for row in records:
    for i in row:
        print(i)
cursor.close()
conn.close()

#--------------------------
print('----------------')
#Query de todos los eventos: SELECT con categoría
openConnection()
cursor = conn.cursor()
id = 1
sql_command = "SELECT evento_data.id, evento_data.nombre, evento_data.precio, evento_data.path_foto_p, categoria.nombre FROM ((evento_data INNER JOIN evento_categoria ON evento_data.id = evento_categoria.id_evento) INNER JOIN categoria ON evento_categoria.id_categoria = categoria.id) WHERE categoria.id = %s;"
cursor.execute(sql_command, (id, ))
records = cursor.fetchall()
for row in records:
    id = row[0]
    for i in row:
        print(i)
cursor.close()
conn.close()
#--------------------------
print('----------------')
#Query de todos los eventos: SELECT sin categoría
openConnection()
cursor = conn.cursor()
sql_command = "SELECT evento_data.id, evento_data.nombre, evento_data.precio, evento_data.path_foto_p, categoria.nombre FROM ((evento_data INNER JOIN evento_categoria ON evento_data.id = evento_categoria.id_evento) INNER JOIN categoria ON evento_categoria.id_categoria = categoria.id);"
cursor.execute(sql_command, )
records = cursor.fetchall()
for row in records:
    for i in row:
        print(i)
cursor.close()
conn.close()

#--------------------------
print('----------------')
#Query de la info del evento
openConnection()
cursor = conn.cursor()
id = 2
sql_command = "SELECT * FROM public.evento_data WHERE evento_data.id = %s;"
cursor.execute(sql_command, (id, ))
records = cursor.fetchall()
for row in records:
    for i in row:
        print(i)
cursor.close()
conn.close()

#--------------------------
print('----------------')
#Query de evento seleccionado: SELECT para información actividad pero de comentarios
openConnection()
cursor = conn.cursor()
id = 1
sql_command = "SELECT user_data.nombre_usuario, evento_comentarios.comentario FROM (user_data INNER JOIN evento_comentarios ON user_data.id = evento_comentarios.id_user) where evento_comentarios.id_evento = %s"
cursor.execute(sql_command, (id, ))
records = cursor.fetchall()
for row in records:
    for i in row:
        print(i)
cursor.close()
conn.close()
#--------------------------INSERT QUERY
print('----------------')
#INSERT DE INFORMACION DE USUARIO LUEGO DE UN REGISTRO
#openConnection()
#cursor = conn.cursor()
#correo = 'mariopisquiy@ufm.edu'
#clave = '54uy23'
#nombre_usuario = 'mariopisquiy'
#pais = 'Guatemala'
#path_foto = 'mariopisquiy_thrw.jpg'
#sql_command = "INSERT INTO public.user_data (correo, contrasena, nombre_usuario, pais, path_foto)VALUES (%s, %s, %s, %s, %s);"
#cursor.execute(sql_command, (correo,clave,nombre_usuario,pais, path_foto, ))
#conn.commit()
#SELECT DEL ID DEL USUARIO CREADO
#sql_command = "SELECT id FROM public.user_data ORDER BY user_data.id DESC LIMIT 1;"
#cursor.execute(sql_command, )
#records = cursor.fetchall()
#for row in records:
#    id_evento = row[0]
#cursor.close()
#conn.close()
#--------------------------
print('----------------')
#INSERT informacion de evento
#openConnection()
#cursor = conn.cursor()
#nombre = "Como hacer query's desde PostgresSQL"
#description = "Juango a un joven ingeniero de Computer Science, y aprende de como hacer diferentes varias querys para diferente tipos de relaciones."
#fecha = "2021-11-27"
#hora = "15:00:00"
#precio = 150
#path_foto_p = "berkejbn.jpg"
#categoria = 3
#sql_command = "INSERT INTO public.evento_data(nombre, description, fecha, hora, precio, path_foto_p)VALUES (%s, %s, %s, %s, %s, %s);"
#cursor.execute(sql_command, (nombre, description, fecha, hora, precio, path_foto_p, ))
#conn.commit()
#SELECT DEL ID DEL EVENTO CREADO
#sql_command = "SELECT id FROM public.evento_data ORDER BY evento_data.id DESC LIMIT 1;"
#cursor.execute(sql_command, )
#records = cursor.fetchall()
#for row in records:
#    id_evento = row[0]
#--- otro insert
#id_evento = 3
#id_categoria = 2
#sql_command = "INSERT INTO public.evento_categoria(id_evento, id_categoria)VALUES(%s, %s);"
#cursor.execute(sql_command, (id_evento, id_categoria, ))
#cursor.close()
#conn.close()
#--------------------------
#--------------------------
print('----------------')
#INSERT de comentarios en el evento
#openConnection()
#cursor = conn.cursor()
#id_evento = 1
#id = 2
#comentario = "No me convence mucho la comida de abuela, creo que no pagaria por verlas."
#sql_command = "INSERT INTO public.evento_comentarios(id_evento, id_user, comentario)VALUES (%s, %s, %s);"
#cursor.execute(sql_command, (id_evento, id, comentario, ))
#conn.commit()
#cursor.close()
#conn.close()
#--------------------------
#--------------------------
print('----------------')
#INSERT de evento creado
#openConnection()
#cursor = conn.cursor()
#id_user = 2
#id_evento = 1
#sql_command = "INSERT INTO public.usuario_evento_creado(id_user, id_evento)VALUES (%s, %s);"
#cursor.execute(sql_command, (id_user, id_evento, ))
#conn.commit()
#cursor.close()
#conn.close()
#--------------------------
#--------------------------
print('----------------')
#INSERT de evento registrado
#openConnection()
#cursor = conn.cursor()
#id_user = 2
#id_evento = 2
#sql_command = "INSERT INTO public.usuario_evento_registrado(id_user, id_evento) VALUES (%s, %s);"
#cursor.execute(sql_command, (id_user, id_evento, ))
#conn.commit()
#cursor.close()
#conn.close()