from flask.helpers import _endpoint_from_view_func, url_for
from flask import Flask, request, redirect
from jinja2 import Template, Environment, FileSystemLoader

File_loader = FileSystemLoader("templates")
env = Environment(loader=File_loader)
app = Flask(__name__)

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
        #foto = request.form.files.get["file"]
        #pais = request.form.get["paises"]
        nombre = request.form["nombre"]
        email = request.form["correo"]
        clave = request.form["clave"]
        if nombre == "" or email == "" or clave == "":
            return template.render(css=css,normalizacioncss=normalizacioncss,logo=logo,scriptregistro=scriptregistro,mensaje="¡Debes llenar todos los campos!")
        return redirect("/inicioSesion")
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
        return redirect("/")
    return template.render(css=css,normalizacioncss=normalizacioncss,logo=logo,mensaje="")

@app.route('/nueva_actividad',methods=["GET","POST"], endpoint="nueva_actividad")
def nueva_actividad():
    css = url_for('static',filename="nueva_actividad_estilos.css")
    normalizacioncss = url_for('static',filename="normalize.css")
    logo = url_for('static',filename="conectados.png")
    template = env.get_template('nueva_actividad.html')
    scriptNuevaActividad = url_for('static',filename="nueva_actividad_scripts.js")
    if request.method == "POST":
        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"]
        #categoria = request.form["categoria"]
        #fecha = request.form["fecha"]
        precio = request.form["precio"]
        #foto1 = request.form["file1"]
        #foto2 = request.form["file2"]
        #foto3 = request.form["file3"]
        #foto4 = request.form["file4"]
        return redirect("/")
    return template.render(css=css,normalizacioncss=normalizacioncss,logo=logo,scriptNuevaActividad=scriptNuevaActividad)

@app.route('/cuenta',methods=["GET","POST"], endpoint="cuenta")
def cuenta():
    css = url_for('static',filename="cuenta.css")
    template = env.get_template('cuenta.html')
    logo = url_for('static',filename="conectados.png")
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
    return template.render(css = css,logo=logo,img1=img1, img2=img2, img3=img3, img4=img4)



if __name__ == '__main__':
    app.run(debug=True)
