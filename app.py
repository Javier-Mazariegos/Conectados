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

UPLOAD_FOLDER = 'C:/Users/mepg1/Documents/GitHub/Conectados/images'
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
    if (request.method == "POST"):
        #var de el id de la categoria
        cate = 0
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
        return template.render(css = css,logoConectados=logoConectados,records = records)
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
        #validar si correo existe y si sí, obtener el id de usuario. SELECT
        session['sesion'] = "id"
        return redirect("/")
    return template.render(css=css,normalizacioncss=normalizacioncss,logo=logo,mensaje="")

@app.route('/nueva_actividad',methods=["GET","POST"], endpoint="nueva_actividad")
def nueva_actividad():
    contadorImagenes = 0
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
        if 'file1' not in request.files or 'file2' not in request.files or 'file3' not in request.files or 'file4' not in request.files:
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
        file = request.files['file2']
        if file.filename == '':
            pass
        if file and allowed_file(file.filename):
            contadorImagenes += 1
            print("Archivo seleccionado")
            filename = nombre + "_foto" + str(contadorImagenes) + "_" + secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file = request.files['file3']
        if file.filename == '':
            pass
        if file and allowed_file(file.filename):
            contadorImagenes += 1
            print("Archivo seleccionado")
            filename = nombre + "_foto" + str(contadorImagenes) + "_" + secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file = request.files['file4']
        if file.filename == '':
            pass
        if file and allowed_file(file.filename):
            contadorImagenes += 1
            print("Archivo seleccionado")
            filename = nombre + "_foto" + str(contadorImagenes) + "_" + secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #INSERT en la tabla de eventos creados.
        return redirect("/mis_actividades")
    return template.render(css=css,normalizacioncss=normalizacioncss,logo=logo,scriptNuevaActividad=scriptNuevaActividad)

@app.route('/cuenta',methods=["GET","POST"], endpoint="cuenta")
def cuenta():
    css = url_for('static',filename="cuenta.css")
    template = env.get_template('cuenta.html')
    logo = url_for('static',filename="conectados.png")
    if (request.method == "DELETE"):
        pass
    #un if de si la variable de loggin tiene algo, y si sí, retornar la info del usuario con respecto al id. SELECT
    #Si no hay algo, enviar a /iniciosesion
    return template.render(css = css, logo = logo)

@app.route('/mis_actividades',methods=["GET","POST"], endpoint="mis_actividades")
def mis_actividades():
    template = env.get_template('mis_actividades.html')
    logo = url_for('static',filename="conectados.png")
    css = url_for('static',filename="mis_actividades.css")
    img1 = url_for('static',filename="hacer1.jpg")
    img2 = url_for('static',filename="hacer2.jpg")
    img3 = url_for('static',filename="hacer3.jpg")
    img4 = url_for('static',filename="hacer4.jpg")
    if (request.method == "POST"):
        pass
    #query que devuelva las actividades creadas por el usuario,
    #querye que devueva las actividades futurias del usuario, registradas. 
    #enviar a NUEVA ACTIVIDAD
    #SI LE DA A UN EVENTO HACER LO MISMO QUE EN "/", #se da return a info actividad, mandando el id en el return SI ES DE FUTURIOS
    #SI LE DA A LOS EVENTOS DE MIS ACTIVIDADES, ENVIAR A EDITAR_ACTIVDAD
    return template.render(css = css,logo=logo,img1=img1, img2=img2, img3=img3, img4=img4)

@app.route('/informacion_actividad',methods=["GET","POST"], endpoint="informacion_actividad")#tengo que recibir el id del evento seleccionado. 
def informacion_actividad():
    css = url_for('static',filename="informacion_actividad.css")
    template = env.get_template('informacion_actividad.html')
    logo = url_for('static',filename="conectados.png")
    img1 = url_for('static',filename="hacer1.jpg")
    img2 = url_for('static',filename="hacer2.jpg")
    img3 = url_for('static',filename="hacer3.jpg")
    img4 = url_for('static',filename="hacer4.jpg")
    #POR CADA ACCION DE COMENTARIO, ES PROBLE QUE SE TENGA QUE REFERSCAR, Y SE DEBE ESTAR MANDO CONSTANTEMENTE EL ID DEL EVENTO EN EL QUE SE ESTA
    #cuando caigo aquí, debo hacer un select, de la info del evento que traigo del html. 
    #cuando le de a registrarme, hacer insert en la base de datos, donde es: usuario_evento_registrado
    #cuando le de al comentario, insert en la tabla de comentarios. y mandar ID nuevamente del evento
    return template.render(css = css, logo = logo,img1=img1, img2=img2, img3=img3, img4=img4)

@app.route('/editar_actividad',methods=["GET","POST"], endpoint="editar_actividad")
def editar_actividad():
    css = url_for('static',filename="editar_actividad.css")
    template = env.get_template('editar_actividad.html')
    logo = url_for('static',filename="conectados.png")
    img1 = url_for('static',filename="hacer1.jpg")
    img2 = url_for('static',filename="hacer2.jpg")
    img3 = url_for('static',filename="hacer3.jpg")
    img4 = url_for('static',filename="hacer4.jpg")
    if (request.method == "POST"):
        pass
    #RECIBIR EL ID DEL EVENTO
    #si le da a eliminar, hacer una función que le mande correo a todos los usuarios que estan registrados.
    #si le da eliminar comentario, se vuelve a mandar el ID para mantener el ciclo. 
    return template.render(css = css, logo = logo,img1=img1, img2=img2, img3=img3, img4=img4)




if __name__ == '__main__':
    app.run(debug=True)
