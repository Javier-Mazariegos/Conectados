from flask.helpers import _endpoint_from_view_func, url_for
from flask import Flask, request
from jinja2 import Template, Environment, FileSystemLoader

File_loader = FileSystemLoader("templates")
env = Environment(loader=File_loader)
app = Flask(__name__)

@app.route('/',methods=["GET","POST"], endpoint="index")
def index():
    template = env.get_template('index.html')
    return template.render()

@app.route('/registro',methods=["GET","POST"], endpoint="registro")
def regristro():
    css = url_for('static',filename="registroEstilos.css")
    normalizacioncss = url_for('static',filename="normalize.css")
    logo = url_for('static',filename="conectados.png")
    template = env.get_template('registro.html')
    return template.render(css=css,normalizacioncss=normalizacioncss,logo=logo)

@app.route('/inicioSesion',methods=["GET","POST"], endpoint="inicioSesion")
def inicioSesion():
    css = url_for('static',filename="loginEstilos.css")
    normalizacioncss = url_for('static',filename="normalize.css")
    logo = url_for('static',filename="conectados.png")
    template = env.get_template('login.html')
    return template.render(css=css,normalizacioncss=normalizacioncss,logo=logo)



if __name__ == '__main__':
    app.run(debug=True)
