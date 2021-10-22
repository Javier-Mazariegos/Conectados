from flask.helpers import _endpoint_from_view_func, url_for
from flask import Flask, request, redirect, session
from jinja2 import Template, Environment, FileSystemLoader
from jinja2.environment import create_cache
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import psycopg2
conn = ""
def openConnection():# Set up a connection to the postgres server.
    global conn
    conn = psycopg2.connect(host="localhost",
                            database="demoConectados",
                            user="postgres",
                            password="CharleiAlvSql")

UPLOAD_FOLDER = os.getcwd() + '/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

File_loader = FileSystemLoader("templates")
env = Environment(loader=File_loader)
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "contraseña"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/',methods=["GET","POST"], endpoint="index")
def index():
    records = ""
    template = env.get_template('index.html')
    logoConectados = url_for('static',filename="conectados2.png")
    css = url_for('static',filename="styles.css")
    openConnection()
    cursor = conn.cursor()
    sql_command = "SELECT * FROM public.categoria"
    cursor.execute(sql_command, )
    categorias = cursor.fetchall()
    cursor.close()
    conn.close()
    if (request.method == "POST"):
        cate = request.form.get("busqueda")
        if cate == 0:
            openConnection()
            cursor = conn.cursor()
            sql_command = "SELECT evento_data.id, evento_data.nombre, evento_data.precio, evento_data.path_foto_p, categoria.nombre FROM ((evento_data INNER JOIN evento_categoria ON evento_data.id = evento_categoria.id_evento) INNER JOIN categoria ON evento_categoria.id_categoria = categoria.id);"
            cursor.execute(sql_command, )
            records = cursor.fetchall()
            cursor.close()
            conn.close()
        else:
            openConnection()
            cursor = conn.cursor()
            id = cate
            sql_command = "SELECT evento_data.id, evento_data.nombre, evento_data.precio, evento_data.path_foto_p, categoria.nombre FROM ((evento_data INNER JOIN evento_categoria ON evento_data.id = evento_categoria.id_evento) INNER JOIN categoria ON evento_categoria.id_categoria = categoria.id) WHERE categoria.id = %s;"
            cursor.execute(sql_command, (id, ))
            records = cursor.fetchall()
            cursor.close()
            conn.close()
    else:
        openConnection()
        cursor = conn.cursor()
        sql_command = "SELECT evento_data.id, evento_data.nombre, evento_data.precio, evento_data.path_foto_p, categoria.nombre FROM ((evento_data INNER JOIN evento_categoria ON evento_data.id = evento_categoria.id_evento) INNER JOIN categoria ON evento_categoria.id_categoria = categoria.id);"
        cursor.execute(sql_command, )
        records = cursor.fetchall()
        cursor.close()
        conn.close()
    if "sesion" in session:
        return template.render(css = css,logoConectados=logoConectados,records = records, categorias = categorias)
    else:
        return redirect("/inicioSesion")

@app.route('/registro',methods=["GET","POST"], endpoint="registro")
def regristro():
    #Dentro de request 'GET'
    css = url_for('static',filename="registroEstilos.css")
    normalizacioncss = url_for('static',filename="normalize.css")
    logo = url_for('static',filename="conectados.png")
    template = env.get_template('registro.html')
    scriptregistro = url_for('static',filename="scripts.js")
    #Dentro de request 'POST'
    if(request.method == 'POST'):
        #Extracción de los datos del form
        pais = request.form["Pais"] #pais
        nombre = request.form["nombre"] #nombre_usuario
        email = request.form["correo"] #correo
        clave = request.form["clave"] #contrasena
        id_validador = 0
        if 'file' not in request.files:
            print("No se seleccionó ningun archivo 1")
            return template.render(css=css,normalizacioncss=normalizacioncss,logo=logo,scriptregistro=scriptregistro,mensaje="No seleccionó ninguna imagen")
        file = request.files['file']
        if file.filename == '':
            print("No se seleccionó ningun archivo 2")
            return template.render(css=css,normalizacioncss=normalizacioncss,logo=logo,scriptregistro=scriptregistro,mensaje="No seleccionó ninguna imagen")
        if file and allowed_file(file.filename):
            print("Archivo seleccionado")
            filename = nombre + "_" + secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            openConnection()
            cursor = conn.cursor()
            sql_command = "SELECT id FROM public.user_data WHERE  public.user_data.correo = %s;"
            cursor.execute(sql_command, (email, ))
            records = cursor.fetchall()
            for row in records:
                id_validador = row[0]
            cursor.close()
            conn.close()
            if id_validador == 0:
                #INSERT DE INFORMACION DE USUARIO LUEGO DE UN REGISTRO
                openConnection()
                cursor = conn.cursor()
                sql_command = "INSERT INTO public.user_data (correo, contrasena, nombre_usuario, pais, path_foto)VALUES (%s, %s, %s, %s, %s);"
                cursor.execute(sql_command, (email,clave,nombre,pais, filename, ))
                conn.commit()
                #SELECT DEL ID DEL USUARIO CREADO
                sql_command = "SELECT id FROM public.user_data ORDER BY user_data.id DESC LIMIT 1;"
                cursor.execute(sql_command, )
                records = cursor.fetchall()
                for row in records:
                    session['sesion'] = row[0]
                cursor.close()
                conn.close()
                return redirect("/") 
            else:
                return template.render(css=css,normalizacioncss=normalizacioncss,logo=logo,scriptregistro=scriptregistro,mensaje="¡Correo ya utilizado!")       
        return template.render(css=css,normalizacioncss=normalizacioncss,logo=logo,scriptregistro=scriptregistro,mensaje="¡Debes llenar todos los campos!")
    return template.render(css=css,normalizacioncss=normalizacioncss,logo=logo,scriptregistro=scriptregistro,mensaje="")

@app.route('/inicioSesion',methods=["GET","POST"], endpoint="inicioSesion")
def inicioSesion():
    css = url_for('static',filename="loginEstilos.css")
    normalizacioncss = url_for('static',filename="normalize.css")
    logo = url_for('static',filename="conectados.png")
    template = env.get_template('login.html')
    #Método POST
    if request.method == 'POST':
        email = request.form["correo"]
        clave = request.form["clave"]
        if email == "" or clave == "":
            return template.render(css=css,normalizacioncss=normalizacioncss,logo=logo,mensaje="¡Debes llenar todos los campos!")
        else:
            #SELECT ID DEL USUARIO LOGGIN
            openConnection()
            cursor = conn.cursor()
            sql_command = "SELECT id FROM public.user_data WHERE  public.user_data.correo = %s and public.user_data.contrasena = %s;"
            cursor.execute(sql_command, (email, clave))
            records = cursor.fetchall()
            for row in records:
                session['sesion'] = row[0]
            cursor.close()
            conn.close()
            return redirect("/")
    return template.render(css=css,normalizacioncss=normalizacioncss,logo=logo,mensaje="")

@app.route('/nueva_actividad',methods=["GET","POST"], endpoint="nueva_actividad")
def nueva_actividad():
    css = url_for('static',filename="nueva_actividad_estilos.css")
    normalizacioncss = url_for('static',filename="normalize.css")
    logo = url_for('static',filename="conectados.png")
    template = env.get_template('nueva_actividad.html')
    scriptNuevaActividad = url_for('static',filename="nueva_actividad_scripts.js")
    #RECIBIR O RECORDAR TENER LE ID DEL USUARIO
    if request.method == "POST":
        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"]
        categoria = request.form.get("categoria")
        fecha_hora = datetime.strptime(request.form['fecha'], "%Y-%m-%dT%H:%M")
        fecha = str(fecha_hora.day) + "-" +str(fecha_hora.month) + "-" + str(fecha_hora.year)
        if fecha_hora.minute < 10:
            hora = str(fecha_hora.hour) + ":0" + str(fecha_hora.minute)
        else:
            hora = str(fecha_hora.hour) + ":" + str(fecha_hora.minute)
        precio = request.form["precio"]
        if 'file1' not in request.files:
            print("No se seleccionó ningun archivo 1")
            return template.render(css=css,normalizacioncss=normalizacioncss,logo=logo,scriptNuevaActividad=scriptNuevaActividad)
        file = request.files['file1']
        if file.filename == '':
            print("No se seleccionó ningun archivo 2")
            return template.render(css=css,normalizacioncss=normalizacioncss,logo=logo,scriptNuevaActividad=scriptNuevaActividad)
        if file and allowed_file(file.filename):
            print("Archivo seleccionado")
            filename = nombre + "_fotoPortada_" + secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #INSERT en la tabla de eventos creados.
        openConnection()
        cursor = conn.cursor()
        sql_command = "INSERT INTO public.evento_data(nombre, description, fecha, hora, precio, path_foto_p)VALUES (%s, %s, %s, %s, %s, %s);"
        cursor.execute(sql_command, (nombre, descripcion, fecha, hora, precio, filename, ))
        conn.commit()
        #SELECT DEL ID DEL EVENTO CREADO
        sql_command = "SELECT id FROM public.evento_data ORDER BY evento_data.id DESC LIMIT 1;"
        cursor.execute(sql_command, )
        records = cursor.fetchall()
        id_evento = ""
        for row in records:
            id_evento = row[0]
        #--- otro insert
        sql_command = "INSERT INTO public.evento_categoria(id_evento, id_categoria)VALUES(%s, %s);"
        cursor.execute(sql_command, (id_evento, categoria, ))
        id_user = session["sesion"]
        sql_command = "INSERT INTO public.usuario_evento_creado(id_user, id_evento)VALUES (%s, %s);"
        cursor.execute(sql_command, (id_user, id_evento, ))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect("/mis_actividades")
    return template.render(css=css,normalizacioncss=normalizacioncss,logo=logo,scriptNuevaActividad=scriptNuevaActividad)

@app.route('/cuenta',methods=["GET","POST", "DELETE"], endpoint="cuenta")#hay un delete/ eliminar cuenta
def cuenta():
    css = url_for('static',filename="cuenta.css")
    template = env.get_template('cuenta.html')
    logo = url_for('static',filename="conectados.png")
    id = ""
    if (request.method == "DELETE"):
        #DELETE
        return redirect("/inicioSesion")
    else:
        openConnection()
        cursor = conn.cursor()
        if "sesion" in session:
            id = session["sesion"]
            sql_command = "SELECT correo, nombre_usuario, pais FROM public.user_data WHERE  public.user_data.id = %s;"
            cursor.execute(sql_command, (id, ))
            records = cursor.fetchall()
            cursor.close()
            conn.close()
            return template.render(css = css, logo = logo, records = records)
        else:
            return redirect("/inicioSesion")

@app.route('/mis_actividades',methods=["GET","POST","DELETE"], endpoint="mis_actividades")#hay DELETE/ evento registrado por boton. / evento por pasar fecha
def mis_actividades():
    template = env.get_template('mis_actividades.html')
    logo = url_for('static',filename="conectados.png")
    css = url_for('static',filename="mis_actividades.css")
    CREADOS = ""
    REGISTRADOS = ""
    if (request.method == "DELETE"):
        if request.form.get('eliminar') == 'eliminar':
            idActividad = request.form["id"]
            #DELETE por boton de eliminar evento registrado
            openConnection()
            cursor = conn.cursor()
            sql_command = "DELETE FROM public.usuario_evento_registrado WHERE usuario_evento_registrado.id_evento = %s"
            cursor.execute(sql_command, (idActividad, ))
            conn.commit()
            cursor.close()
            conn.close()
        
    else:
        #ID DE EVENTOS CREADOS:
        openConnection()
        cursor = conn.cursor()
        id = session["sesion"]
        ids = []
        sql_command = "SELECT id_evento FROM usuario_evento_creado where id_user = %s"
        cursor.execute(sql_command, (id, ))
        records = cursor.fetchall()
        for row in records:
            ids.append(row[0])
        cursor.close()
        conn.close()
        ids = tuple(ids)
        #MIS EVENTOS CREADOS:
        openConnection()
        cursor = conn.cursor()
        sql_command = "SELECT evento_data.id, evento_data.nombre, evento_data.precio, evento_data.path_foto_p, categoria.nombre FROM ((evento_data INNER JOIN evento_categoria ON evento_data.id = evento_categoria.id_evento) INNER JOIN categoria ON evento_categoria.id_categoria = categoria.id) WHERE evento_data.id IN %s;"
        cursor.execute(sql_command, (ids, ))
        CREADOS = cursor.fetchall()
        cursor.close()
        conn.close()
        #MIS EVENTOS REGISTRADOS IDS
        openConnection()
        cursor = conn.cursor()
        id = session["sesion"]
        ids = []
        sql_command = "SELECT id_evento FROM usuario_evento_registrado where id_user = %s"
        cursor.execute(sql_command, (id, ))
        records = cursor.fetchall()
        for row in records:
            ids.append(row[0])
        cursor.close()
        conn.close()
        ids = tuple(ids)
        #MIS EVENTOS REGISTRADOS
        openConnection()
        cursor = conn.cursor()
        sql_command = "SELECT evento_data.id, evento_data.nombre, evento_data.precio, evento_data.path_foto_p, evento_data.fecha, evento_data.hora, categoria.nombre FROM ((evento_data INNER JOIN evento_categoria ON evento_data.id = evento_categoria.id_evento) INNER JOIN categoria ON evento_categoria.id_categoria = categoria.id) WHERE evento_data.id IN %s;"
        cursor.execute(sql_command, (ids, ))
        REGISTRADOS = cursor.fetchall()
        currentTime = datetime.now()
        currentTime = (currentTime.year * 10000000000) + (currentTime.month * 100000000) +  (currentTime.day * 1000000)
        for row in REGISTRADOS:
            print(row)
            fechaEvento = row[4]
            fechaEvento = datetime.strptime(fechaEvento,'%Y-%m-%d')
            fechaEvento = (fechaEvento.year * 10000000000) + (fechaEvento.month * 100000000) +  (fechaEvento.day * 1000000)
            if (currentTime - fechaEvento == 15):
                id_Actividad = row[0]
                #DELETE por fecha
                pass
        #datetime para ver si el evento se guarad o no. 
        #recorrer el array y 
        #for que entre a REGISTRADOS, row in regist
        #row[4] obtienes la fecha. y validad que esa fecha no se haya pasado por 30 días.
        # si esta en rango de fecha aceptable, en otra variable guardas row. REGISTRADOS2.append(row)
        cursor.close()
        conn.close()
    return template.render(css = css,logo=logo,creados=CREADOS, registrados = REGISTRADOS)

@app.route('/informacion_actividad/<idActividad>',methods=["GET","POST"], endpoint="informacion_actividad")#tengo que recibir el id del evento seleccionado. 
def informacion_actividad(idActividad=None):
    css = url_for('static',filename="informacion_actividad.css")
    template = env.get_template('informacion_actividad.html')
    logo = url_for('static',filename="conectados.png")
    if (request.method == "POST"):
        if request.form.get('Registrarme') == 'Registrarme':
            openConnection()
            cursor = conn.cursor()
            id_user = session["sesion"]
            id_evento = idActividad
            sql_command = "INSERT INTO public.usuario_evento_registrado(id_user, id_evento) VALUES (%s, %s);"
            cursor.execute(sql_command, (id_user, id_evento, ))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect("mis_actividades")
        if request.form.get('Comentar') == 'Comentar':
            openConnection()
            cursor = conn.cursor()
            id_evento = idActividad
            id = session["sesion"]
            comentario = request.form["comentario"]
            sql_command = "INSERT INTO public.evento_comentarios(id_evento, id_user, comentario)VALUES (%s, %s, %s);"
            cursor.execute(sql_command, (id_evento, id, comentario, ))
            conn.commit()
            cursor.close()
            conn.close()
    openConnection()
    cursor = conn.cursor()
    id = idActividad
    sql_command = "SELECT * FROM public.evento_data WHERE evento_data.id = %s;"
    cursor.execute(sql_command, (id, ))
    informacion = cursor.fetchall()
    cursor.close()
    conn.close()  
    openConnection()
    cursor = conn.cursor()
    id = idActividad
    sql_command = "SELECT user_data.nombre_usuario, evento_comentarios.comentario FROM (user_data INNER JOIN evento_comentarios ON user_data.id = evento_comentarios.id_user) where evento_comentarios.id_evento = %s"
    cursor.execute(sql_command, (id, ))
    comentarios = cursor.fetchall()
    cursor.close()
    conn.close()
    return template.render(css = css, logo = logo,informacion = informacion, comentarios = comentarios)

@app.route('/editar_actividad/<idActividad>',methods=["GET","POST","DELETE"], endpoint="editar_actividad") #idActividad/HAY DELETE/ Comentario y Evento
def editar_actividad(idActividad=None):
    css = url_for('static',filename="editar_actividad.css")
    template = env.get_template('editar_actividad.html')
    logo = url_for('static',filename="conectados.png")
    img1 = url_for('static',filename="hacer1.jpg")
    img2 = url_for('static',filename="hacer2.jpg")
    img3 = url_for('static',filename="hacer3.jpg")
    img4 = url_for('static',filename="hacer4.jpg")
    if (request.method == "DELETE"):
        if request.form.get('eliminarActividad') == 'eliminarActividad':
            #DELETE idActividad
            pass
        if request.form.get('eliminarComentario') == 'eliminarComentario':
            #DELETE idComentario
            idComentario = request.form["idcomentario"]
            openConnection()
            cursor = conn.cursor()
            sql_command = "DELETE FROM public.evento_comentarios WHERE evento_comentario.id = %s"
            cursor.execute(sql_command, (idComentario, ))
            conn.commit()
            cursor.close()
            conn.close()
    openConnection()
    cursor = conn.cursor()
    id = idActividad
    sql_command = "SELECT * FROM public.evento_data WHERE evento_data.id = %s;"
    cursor.execute(sql_command, (id, ))
    informacion = cursor.fetchall()
    cursor.close()
    conn.close()
    openConnection()
    cursor = conn.cursor()
    id = idActividad
    sql_command = "SELECT evento_comentarios.id, user_data.nombre_usuario, evento_comentarios.comentario FROM (user_data INNER JOIN evento_comentarios ON user_data.id = evento_comentarios.id_user) where evento_comentarios.id_evento = %s"
    cursor.execute(sql_command, (id, ))
    comentarios = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return template.render(css = css, logo = logo,informacion = informacion, comentarios = comentarios)




if __name__ == '__main__':
    app.run(debug=True)
