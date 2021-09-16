from flask.helpers import _endpoint_from_view_func, url_for
from flask import Flask, request
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
    css = url_for('static',filename="registroEstilos.css")
    normalizacioncss = url_for('static',filename="normalize.css")
    logo = url_for('static',filename="conectados.png")
    template = env.get_template('registro.html')
    scriptregistro = url_for('static',filename="scripts.js")
    return template.render(css=css,normalizacioncss=normalizacioncss,logo=logo,scriptregistro=scriptregistro)

@app.route('/inicioSesion',methods=["GET","POST"], endpoint="inicioSesion")
def inicioSesion():
    css = url_for('static',filename="loginEstilos.css")
    normalizacioncss = url_for('static',filename="normalize.css")
    logo = url_for('static',filename="conectados.png")
    template = env.get_template('login.html')
    return template.render(css=css,normalizacioncss=normalizacioncss,logo=logo)



if __name__ == '__main__':
    app.run(debug=True)
