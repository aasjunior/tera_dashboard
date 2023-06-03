from flask import render_template, redirect, request, url_for, send_from_directory, Response, send_file
from flask_bcrypt import Bcrypt, check_password_hash
from models.database import *
from .components import *
from .helpers import *
from pymongo import MongoClient
from gridfs import GridFS

client = MongoClient('localhost', 27017)
db = client['clinica_0']
fs = GridFS(db)

def init_app(app, bcrypt):

    @app.route("/", methods=['GET','POST'])
    def index():
        minify_css()
        if request.method == 'POST':
            username = request.form['user-login']
            user = db.Usuarios.find_one({'login': username})
            if user and check_password_hash(user['senha'], request.form['user-password']):
                return redirect(url_for('cadastro_monitor'))
            else:
                return 'Usuário ou senha invalido'
        return render_template("login.html")
    
    @app.route("/dashboard")
    def dashboard():
        return render_template("dashboard.html", **components)
    
    @app.route("/pacientes")
    def pacientes():
        return render_template("pacientes.html", **components)
    
    @app.route("/paciente-dados")
    def paciente_dados():
        return render_template("paciente-dados.html", **components)
      
    @app.route("/paciente-diagnostico")
    def paciente_diagnostico():
        return render_template("paciente-diagnostico.html", **components)
    
    @app.route("/paciente-familiar")
    def paciente_familiar():
        return render_template("paciente-familiar.html", **components)

    @app.route("/cadastro-monitor", methods=['GET', 'POST'])
    def cadastro_monitor():
        if request.method == 'POST':
            form = request.form
            monitor_login = create_monitor_login(bcrypt, form)
            user_id = db.Usuarios.insert_one(monitor_login).inserted_id

            image_file = request.files['foto']
            angle = float(form['angle'])
            encoded_image = encode_image(image_file, angle)

            image_filename = generate_unique_filename('png')
            image_id = fs.put(encoded_image.tostring(), filename=image_filename)

            monitor_dados = create_monitor_dados(form, image_id, user_id)
            db.Monitores.insert_one(monitor_dados)

            image_data = fs.get(image_id).read()

            # enviar a imagem como uma resposta HTTP
            return Response(image_data, mimetype='image/png')

        return render_template("cadastro-monitor.html", **components)
    
    @app.route("/cadastro-clinica")
    def cadastro_clinica():
        return render_template("cadastro-clinica.html", **components)

    @app.route("/static/<path:filename>")
    def static_files(filename):
        return send_from_directory("static", filename)
    
    @app.route("/paciente")
    def paciente():
        return render_template("paciente.html", **components)
    
    @app.route("/consulta-pacientes")
    def consulta_pacientes():
        return render_template("consulta-pacientes.html", **components)
    
    @app.route("/consulta-monitores")
    def consulta_monitores():
        return render_template("consulta-monitores.html", **components)