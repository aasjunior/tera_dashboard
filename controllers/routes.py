from flask import render_template, redirect, request, url_for, send_from_directory
from .components import *
from pymongo import MongoClient

client = MongoClient('localhost', 27017)

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
    
    @app.route("/consulta-monitores")
    def consulta_monitores():
        components = {
            'sidebar': render_sidebar,
            'welcome_card': render_welcome_card,
            'header_title' : render_header_title,
        }
        # Acessa a coleção 'dados' no banco de dados 'monitor'
        db = client['monitor']
        collection = db['dados']
        
        # Obtém os últimos 10 registros em ordem decrescente
        registros = collection.find().sort('_id', -1).limit(10)
        
        # Renderiza o template HTML passando os registros para exibição na tabela
        return render_template("consulta-monitores.html", **components, registros=registros)