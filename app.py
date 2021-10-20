from flask.helpers import _endpoint_from_view_func, url_for
from flask import Flask, request, redirect, flash
from jinja2 import Template, Environment, FileSystemLoader
from werkzeug.utils import secure_filename
import os
from datetime import datetime

UPLOAD_FOLDER = 'C:/Users/mepg1/Documents/GitHub/Conectados/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

File_loader = FileSystemLoader("templates")
env = Environment(loader=File_loader)
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/',methods=["GET","POST"], endpoint="index")
def index():
    template = env.get_template('index.html')
    icono = url_for('static',filename="hamburgesa.png")
    logoConectados = url_for('static',filename="conectados2.png")
    css = url_for('static',filename="styles.css")
    img1 = url_for('static',filename="hacer1.jpg")
    img2 = url_for('static',filename="hacer2.jpg")
    img3 = url_for('static',filename="hacer3.jpg")
    img4 = url_for('static',filename="hacer4.jpg")
    #una query de select que devuelva las categorias, con nombre y id.
    #una query de select donde vaya a todos los eventos creados y publicarlos. si la value == 0
                #trayendo la info y id. y guardarlo en un dict, para mandarlo de nuevo. 
    #se da return a info actividad, mandando el id en el return. #si ya estoy registrado, bandera de registrado
    return template.render(css = css,logoConectados=logoConectados,img1=img1, img2=img2, img3=img3, img4=img4,icono=icono)

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
        #pais = request.form.get["paises"]
        nombre = request.form["nombre"] #nombre_usuario
        email = request.form["correo"] #correo
        clave = request.form["clave"] #contrasena
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
            #query de insert en user_data toda la info y select del id del usuario INSERT
            #validacion de que el correo no exista ya. SELECT
            return redirect("/")        
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
        #foto1 = request.form["file1"]
        #foto2 = request.form["file2"]
        #foto3 = request.form["file3"]
        #foto4 = request.form["file4"]
        #INSERT en la tabla de eventos creados. 
        return redirect("/mis_actividades")
    return template.render(css=css,normalizacioncss=normalizacioncss,logo=logo,scriptNuevaActividad=scriptNuevaActividad)

@app.route('/cuenta',methods=["GET","POST"], endpoint="cuenta")
def cuenta():
    css = url_for('static',filename="cuenta.css")
    template = env.get_template('cuenta.html')
    logo = url_for('static',filename="conectados.png")
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
    #RECIBIR EL ID DEL EVENTO
    #si le da a eliminar, hacer una función que le mande correo a todos los usuarios que estan registrados.
    #si le da eliminar comentario, se vuelve a mandar el ID para mantener el ciclo. 
    return template.render(css = css, logo = logo,img1=img1, img2=img2, img3=img3, img4=img4)




if __name__ == '__main__':
    app.run(debug=True)
