from flask import render_template, redirect, request, url_for, send_from_directory
from .components import *
from pymongo import MongoClient
import math

client = MongoClient('localhost', 27017)
db = client['monitor']
collection = db['dados']

def init_app(app):

    @app.route("/")
    def index():
        return render_template("login.html")
    
    @app.route("/dashboard")
    def dashboard():
        components = {
            'sidebar': render_sidebar,
            'welcome_card': render_welcome_card,
            'daily_record': render_daily_record,
            'annual_record': render_annual_record,
            'monthly_record': render_monthly_record,
            'header_title' : render_header_title,
        }
        return render_template("dashboard.html", **components)
    
    @app.route("/pacientes")
    def pacientes():
        components = {
            'sidebar': render_sidebar,
            'welcome_card': render_welcome_card,
            'header_title' : render_header_title,
            'crisis_patient_card' : render_crisis_patient_card,
            'offline_patient_card' : render_offline_patient_card,
        }
        return render_template("pacientes.html", **components)
    
    @app.route("/paciente-dados")
    def paciente_dados():
        components = {
            'sidebar': render_sidebar,
            'welcome_card': render_welcome_card,
            'upload_image': render_upload_image,
            'header_title' : render_header_title,
            'progress_bar' : render_progress_bar,
        }
        return render_template("paciente-dados.html", **components)
      
    @app.route("/paciente-diagnostico")
    def paciente_diagnostico():
        components = {
            'sidebar': render_sidebar,
            'welcome_card': render_welcome_card,
            'upload_image': render_upload_image,
            'header_title' : render_header_title,
            'progress_bar' : render_progress_bar,
        }
        return render_template("paciente-diagnostico.html", **components)
    
    @app.route("/paciente-familiar")
    def paciente_familiar():
        components = {
            'sidebar': render_sidebar,
            'welcome_card': render_welcome_card,
            'upload_image': render_upload_image,
            'header_title' : render_header_title,
            'progress_bar' : render_progress_bar,
        }
        return render_template("paciente-familiar.html", **components)
    
    @app.route("/cadastro-monitor")
    def cadastro_monitor():
        components = {
            'sidebar': render_sidebar,
            'welcome_card': render_welcome_card,
            'upload_image': render_upload_image,
            'header_title' : render_header_title,
            'progress_bar' : render_progress_bar,
        }
        return render_template("cadastro-monitor.html", **components)
    
    @app.route("/cadastro-clinica")
    def cadastro_clinica():
        components = {
            'sidebar': render_sidebar,
            'welcome_card': render_welcome_card,
            'upload_image': render_upload_image,
            'header_title' : render_header_title,
            'progress_bar' : render_progress_bar,
        }
        return render_template("cadastro-clinica.html", **components)
    
    @app.route("/upload-imagem", methods=["GET", "POST"])
    def upload_imagem():
        if request.method == "POST":
            # Salvar a imagem e fazer qualquer processamento necessário
            # Aqui, você pode usar bibliotecas como Pillow para rotacionar a imagem
            
            # Após salvar a imagem, redirecionar de volta para a tela anterior
            return redirect(url_for("paciente_dados"))
    
        # Se o método for GET, renderizar a tela de upload de imagem
        return render_template("upload-imagem.html")

    @app.route("/overlay.html")
    def overlay():
        return render_template("overlay.html")

    @app.route("/static/<path:filename>")
    def static_files(filename):
        return send_from_directory("static", filename)
    
    @app.route("/paciente")
    def paciente():
        components = {
            'sidebar': render_sidebar,
            'welcome_card': render_welcome_card,
            'header_title' : render_header_title,
        }
        return render_template("paciente.html", **components)
    
    @app.route("/consulta-pacientes")
    def consulta_pacientes():
        components = {
            'sidebar': render_sidebar,
            'welcome_card': render_welcome_card,
            'header_title' : render_header_title,
        }
        return render_template("consulta-pacientes.html", **components)
    
    @app.route('/consulta-monitores')
    def consulta_monitores():
        components = {
            'sidebar': render_sidebar,
            'welcome_card': render_welcome_card,
            'header_title' : render_header_title,
        }
        
        total_registros = collection.count_documents({})
        num_paginas = math.ceil(total_registros / 10)  # Calcula o número total de páginas

        # Obtém os registros da página atual
        page_num = request.args.get('page', default=1, type=int)
        skip_num = (page_num - 1) * 10
        registros = list(collection.find().sort('_id', -1).skip(skip_num).limit(10))

        # Renderiza o template HTML passando os registros e informações de paginação
        return render_template('consulta-monitores.html', registros=registros, num_paginas=num_paginas, page_num=page_num, **components)

    
    @app.route('/pagina/<int:page_num>')
    def pagina(page_num=1):
        components = {
            'sidebar': render_sidebar,
            'welcome_card': render_welcome_card,
            'header_title' : render_header_title,
        }

        total_registros = collection.count_documents({})
        num_paginas = math.ceil(total_registros / 10)  # Calcula o número total de páginas

        skip_num = (page_num - 1) * 10
        registros = list(collection.find().sort('_id', -1).skip(skip_num).limit(10))

        return render_template('consulta-monitores.html', registros=registros, num_paginas=num_paginas, page_num=page_num, **components)