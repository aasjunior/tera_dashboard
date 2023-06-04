from flask import render_template, redirect, request, url_for, send_from_directory, Response, session
from flask_bcrypt import Bcrypt, check_password_hash
from models.database import *
from .utils.components import *
from .utils.helpers import *
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from gridfs import GridFS

def init_app(app, bcrypt):
    @app.route("/")
    def index():
        if 'logado' in session and session['logado'] == True:
            return redirect(url_for('dashboard'))
        else:
            return render_template("login.html")
        
    @app.route("/login")
    def login():
        return redirect(url_for('index'))
    
    @app.route("/dashboard")
    def dashboard():
        if 'logado' not in session or session['logado'] != True:
            return redirect(url_for('login'))
        else:
            username = session['username']
            return render_template("dashboard.html", **components, username=username)
    
    @app.route("/pacientes")
    def pacientes():
        if 'logado' not in session or session['logado'] != True:
            return redirect(url_for('login'))
        else:
            username = session['username']
            return render_template("pacientes.html", **components, username=username)
    
    @app.route("/paciente-dados")
    def paciente_dados():
        if 'logado' not in session or session['logado'] != True:
            return redirect(url_for('login'))
        else:
            username = session['username']
            return render_template("paciente-dados.html", **components, username=username)
      
    @app.route("/paciente-diagnostico")
    def paciente_diagnostico():
        if 'logado' not in session or session['logado'] != True:
            return redirect(url_for('login'))
        else:
            username = session['username']
            return render_template("paciente-diagnostico.html", **components, username=username)
    
    @app.route("/paciente-familiar")
    def paciente_familiar():
        if 'logado' not in session or session['logado'] != True:
            return redirect(url_for('login'))
        else:
            username = session['username']
            return render_template("paciente-familiar.html", **components, username=username)

    @app.route("/cadastro-monitor", methods=['GET', 'POST'])
    def cadastro_monitor():
        if 'logado' not in session or session['logado'] != True:
            return redirect(url_for('login'))
        else:
            username = session['username']
            return render_template("cadastro-monitor.html", **components, username=username)
    
    @app.route("/cadastro-clinica")
    def cadastro_clinica():
        if 'logado' not in session or session['logado'] != True:
            return redirect(url_for('login'))
        else:
            username = session['username']
            return render_template("cadastro-clinica.html", **components, username=username)

    @app.route("/static/<path:filename>")
    def static_files(filename):
        if 'logado' not in session or session['logado'] != True:
            return redirect(url_for('login'))
        else:
            username = session['username']
            return send_from_directory("static", filename, username=username)
    
    @app.route("/paciente")
    def paciente():
        if 'logado' not in session or session['logado'] != True:
            return redirect(url_for('login'))
        else:
            username = session['username']
            return render_template("paciente.html", **components, username=username)
    
    @app.route("/consulta-pacientes")
    def consulta_pacientes():
        if 'logado' not in session or session['logado'] != True:
            return redirect(url_for('login'))
        else:
            username = session['username']
            return render_template("consulta-pacientes.html", **components, username=username)
    
    @app.route("/consulta-monitores")
    def consulta_monitores():
        if 'logado' not in session or session['logado'] != True:
            return redirect(url_for('login'))
        else:
            username = session['username']
            return render_template("consulta-monitores.html", **components, username=username)
    
    @app.route("/valida-login", methods=['GET', 'POST'])
    def valida_login():
        if request.method == 'POST':
            try:
                client = conn('localhost', 27017, 'tera')
                db = client.get_default_database()
                username = request.form['user-login']
                user = db.Usuarios.find_one({'login': username})
                client.close()
                if user and check_password_hash(user['senha'], request.form['user-password']):
                    return setsession(user)
                else:
                    return 'Usuário ou senha invalido'
            except PyMongoError as e:
                return f'Ocorreu um erro com a tentativa de conexão: {e}'
            
    @app.route("/logout")
    def logout():
        # Limpa a sessão
        session.clear()
        # Redireciona o usuário para a página de login
        return redirect(url_for('login'))
    
    ## CRUD
    @app.route("/create-monitor", methods=['GET', 'POST'])
    def create_monitor():
        try:
            tera = conn('localhost', 27017, 'tera')
            tera_db = tera.get_default_database()

            if request.method == 'POST':
                form = request.form
                monitor_login = create_monitor_login(bcrypt, form, session['clinica_db'])
                user_id = tera_db.Usuarios.insert_one(monitor_login).inserted_id
                tera.close()

                client = conn('localhost', 27017, session['clinica_db'])
                db = client.get_default_database()
                fs = GridFS(db)

                image_file = request.files['foto']
                angle = float(form['angle'])
                encoded_image = encode_image(image_file, angle)

                image_filename = generate_unique_filename('png')
                image_id = fs.put(encoded_image.tostring(), filename=image_filename)

                monitor_dados = create_monitor_dados(form, image_id, user_id)
                
                if(db.Monitores.insert_one(monitor_dados).inserted_id):
                    return f'Monitor cadastrado com sucesso'
                else:
                    return 'Erro ao tentar inserir os dados do monitor'
                
        except Exception as e:
            # exibe a mensagem de erro
            print(f'Erro: {e}')
            return f'Erro: {e}'