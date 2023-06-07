from flask import render_template, redirect, request, url_for, send_from_directory, Response, session
from flask_bcrypt import Bcrypt, check_password_hash
from models.database import *
from .utils.components import *
from .utils.helpers import *
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from gridfs import GridFS
from io import BytesIO
from datetime import datetime, timedelta
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import math
import os

def init_app(app, bcrypt):
    @app.route("/")
    def index():
        clear_session()
        if 'logado' in session and session['logado'] == True:
            return redirect(url_for('dashboard'))
        else:
            return render_template("login.html")
        
    @app.route("/login")
    def login():
        clear_session()
        return redirect(url_for('index'))
    
    @app.route("/dashboard")
    def dashboard():
        clear_session()
        if 'logado' not in session or session['logado'] != True:
            return redirect(url_for('login'))
        else:
            client = conn('localhost', 27017, session['clinica_db'])
            db = client.get_default_database()

            # Contagem total de pacientes
            total_pacientes = db.Pacientes.count_documents({})
            
            # Consultar os registros de humor nas últimas 24 horas
            resultados = consultar_registros(db)
            anual = consultar_registros_anual(db)
            panel_crisis = panelCrisis(db)
            
            return render_template("dashboard.html", **components, total_pacientes=total_pacientes, resultados=resultados, anual=anual, panel_crisis=panel_crisis)

    
    @app.route("/pacientes")
    def pacientes():
        clear_session()
        if 'logado' not in session or session['logado'] != True:
            return redirect(url_for('login'))
        else:
            return render_template("pacientes.html", **components)
    
    @app.route("/paciente-dados", methods=['GET', 'POST'])
    def paciente_dados():
        if 'logado' not in session or session['logado'] != True:
            return redirect(url_for('login'))
        else:
            if request.method == 'POST':
                session['paciente_dados'] = request.form
                if 'foto' in request.files:
                    imagem_paciente = request.files['foto']
                    filename = secure_filename(imagem_paciente.filename)
                    imagem_paciente.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    session['imagem_paciente'] = filename
                return redirect(url_for('paciente_diagnostico'))
            return render_template("paciente-dados.html", **components)
      
    @app.route("/paciente-diagnostico", methods=['GET', 'POST'])
    def paciente_diagnostico():
        if 'logado' not in session or session['logado'] != True:
            return redirect(url_for('login'))
        else:
            medicamentos = ['Fluoxetina', 'Naltrexona', 'Bupropiona', 'Acamprosato', 'Metadona']

            if request.method == 'POST':
                session['dados_medicos'] = request.form
                session['hora-lembretes'] = request.form.getlist('hora-lembrete[]')
                session['lembretes'] = request.form.getlist('lembrete[]')
                hora_lembrete_medicamento = request.form.getlist('hora-lembrete-medicamento[]')
                lembrete_medicamento = request.form.getlist('lembrete-medicamento[]')
                session['lembretes_medicamentos'] = list(zip(hora_lembrete_medicamento, lembrete_medicamento))
                return redirect(url_for('paciente_familiar'))
            return render_template("paciente-diagnostico.html", **components, medicamentos=medicamentos, lembretes=session.get('lembretes', []))

    
    @app.route("/paciente-familiar", methods=['GET', 'POST'])
    def paciente_familiar():
        if 'logado' not in session or session['logado'] != True:
            return redirect(url_for('login'))
        else:
            if request.method == 'POST':
                session['familiar'] = request.form
                if 'foto' in request.files:
                    imagem_familiar = request.files['foto']
                    filename = secure_filename(imagem_familiar.filename)
                    imagem_familiar.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    session['imagem_familiar'] = filename

                if 'paciente_dados' in session and 'dados_medicos' in session:
                    client = conn('localhost', 27017, session['clinica_db'])
                    db = client.get_default_database()
                    fs = GridFS(db)

                    if 'imagem_paciente' in session:
                        filename = session['imagem_paciente']
                        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        with open(filepath, 'rb') as f:
                            image_file = FileStorage(f)
                            angle = float(session['paciente_dados']['angle'])
                            encoded_image = encode_image(image_file, angle)
                            image_filename = generate_unique_filename('png')
                            pacienteimage_id = fs.put(encoded_image.tostring(), filename=image_filename)
                            paciente_dados = create_paciente_dados(pacienteimage_id)

                            paciente_id = db.Pacientes.insert_one(paciente_dados).inserted_id
                            dados_medicos = create_dados_medicos(paciente_id)
                            db.DadosMedicos.insert_one(dados_medicos)

                    if 'imagem_familiar' in session:
                        filename = session['imagem_paciente']
                        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        with open(filepath, 'rb') as f:
                            image_file = FileStorage(f)
                            angle = float(session['familiar']['angle'])
                            encoded_image = encode_image(image_file, angle)
                            image_filename = generate_unique_filename('png')
                            familiarimage_id = fs.put(encoded_image.tostring(), filename=image_filename)
                            familiar = create_familiar(familiarimage_id, paciente_id)
                            db.Familiares.insert_one(familiar)

                return redirect(url_for('dashboard'))
            return render_template("paciente-familiar.html", **components)

    @app.route("/cadastro-monitor", methods=['GET', 'POST'])
    def cadastro_monitor():
        clear_session()
        if 'logado' not in session or session['logado'] != True:
            return redirect(url_for('login'))
        elif 'administrador' not in session['nivel']:
            return redirect(url_for('acesso_recusado'))
        else:
            return render_template("cadastro-monitor.html", **components)
    
    @app.route("/cadastro-clinica")
    def cadastro_clinica():
        clear_session()
        if 'logado' not in session or session['logado'] != True:
            return redirect(url_for('login'))
        elif 'administrador' not in session['nivel']:
            return redirect(url_for('acesso_recusado'))
        else:
            username = session['username']
            return render_template("cadastro-clinica.html", **components, username=username)

    @app.route("/static/<path:filename>")
    def static_files(filename):
        clear_session()
        if 'logado' not in session or session['logado'] != True:
            return redirect(url_for('login'))
        else:
            username = session['username']
            return send_from_directory("static", filename, username=username)
    
    @app.route("/paciente")
    def paciente():
        clear_session()
        if 'logado' not in session or session['logado'] != True:
            return redirect(url_for('login'))
        else:
            username = session['username']
            return render_template("paciente.html", **components, username=username)
    
    @app.route("/consulta-pacientes")
    def consulta_pacientes():
        clear_session()
        if 'logado' not in session or session['logado'] != True:
            return redirect(url_for('login'))
        else:
            return render_template("consulta-pacientes.html", **components)
    
    @app.route("/consulta-monitores")
    def consulta_monitores():
        clear_session()
        if 'logado' not in session or session['logado'] != True:
            return redirect(url_for('login'))
        elif 'administrador' not in session['nivel']:
            return redirect(url_for('acesso_recusado'))
        else:
            # Conexão com a coleção "Monitores" do banco de dados "clinica_0"
            client_monitores = conn('localhost', 27017, session['clinica_db'])
            db_monitores = client_monitores.get_default_database()
            
            # Conexão com a coleção "Usuarios" do banco de dados "telra"
            client_usuarios = conn('localhost', 27017, 'tera')
            db_usuarios = client_usuarios.get_default_database()

            total_registros = db_monitores.Monitores.count_documents({})
            num_paginas = math.ceil(total_registros / 10)  # Calcula o número total de páginas

            # Obtém os registros da página atual
            page_num = request.args.get('page', default=1, type=int)
            skip_num = (page_num - 1) * 10
            
            registros = list(db_monitores.Monitores.find().sort('_id', -1).skip(skip_num).limit(10))
            
            # Atualiza os registros com dados do banco de dados "telra"
            for registro in registros:
                usuario_id = registro["usuario_id"]
                usuario = db_usuarios.Usuarios.find_one({"_id": usuario_id})
                if usuario:
                    registro["login"] = usuario["login"]
                    registro["data_cadastro"] = usuario["data_cadastro"]
            
            return render_template("consulta-monitores.html", **components, num_paginas=num_paginas, page_num=page_num, registros=registros)
    
    @app.route('/pagina/<int:page_num>')
    def pagina(page_num=1):
        # Conexão com a coleção "Monitores" do banco de dados "clinica_0"
            client_monitores = conn('localhost', 27017, session['clinica_db'])
            db_monitores = client_monitores.get_default_database()
            
            # Conexão com a coleção "Usuarios" do banco de dados "telra"
            client_usuarios = conn('localhost', 27017, 'tera')
            db_usuarios = client_usuarios.get_default_database()

            total_registros = db_monitores.Monitores.count_documents({})
            num_paginas = math.ceil(total_registros / 10)  # Calcula o número total de páginas

            # Obtém os registros da página atual
            page_num = request.args.get('page', default=1, type=int)
            skip_num = (page_num - 1) * 10
            
            registros = list(db_monitores.Monitores.find().sort('_id', -1).skip(skip_num).limit(10))
            
            # Atualiza os registros com dados do banco de dados "telra"
            for registro in registros:
                usuario_id = registro["usuario_id"]
                usuario = db_usuarios.Usuarios.find_one({"_id": usuario_id})
                if usuario:
                    registro["login"] = usuario["login"]
                    registro["data_cadastro"] = usuario["data_cadastro"]
            
            return render_template("consulta-monitores.html", **components, num_paginas=num_paginas, page_num=page_num, registros=registros)
    
    @app.route("/acesso-recusado")
    def acesso_recusado():
        return render_template("acesso-recusado.html", **components)
    
    @app.route("/valida-login", methods=['GET', 'POST'])
    def valida_login():
        clear_session()
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
        clear_session()
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
                    client.close()
                    # return f'Monitor cadastrado com sucesso'
                    return 'success'
                else:
                    return 'Erro ao tentar inserir os dados do monitor'
                
        except Exception as e:
            print(f'Erro: {e}')
            return f'Erro: {e}'
        
        
    def clear_session():
        # Obtém a URL da página atual
        url = request.path

        # Verifica se a URL não corresponde a uma das páginas do formulário de cadastro
        if url not in ['/paciente-dados', '/paciente-diagnostico', '/paciente-familiar']:
            # Remove as variáveis de sessão relacionadas ao cadastro do paciente
            session.pop('paciente_dados', None)
            session.pop('dados_medicos', None)
            session.pop('familiar', None)

            # Remove as imagens armazenadas temporariamente
            if 'imagem_paciente' in session:
                filename = session.pop('imagem_paciente')
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                os.remove(filepath)
            if 'imagem_familiar' in session:
                filename = session.pop('imagem_familiar')
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                os.remove(filepath)
