from flask import render_template, request
from .components import *

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
        }
        return render_template("dashboard.html", **components)
    
    @app.route("/pacientes")
    def pacientes():
        components = {
            'sidebar': render_sidebar,
            'welcome_card': render_welcome_card,
        }
        return render_template("pacientes.html", **components)
    
    @app.route("/paciente-dados")
    def paciente_dados():
        components = {
            'sidebar': render_sidebar,
            'welcome_card': render_welcome_card,
            'upload_image': render_upload_image,
        }
        return render_template("paciente-dados.html", **components)
    
    @app.route("/upload-imagem", methods=["GET", "POST"])
    def upload_imagem():
        if request.method == "POST":
            # Salvar a imagem e fazer qualquer processamento necessário
            # Aqui, você pode usar bibliotecas como Pillow para rotacionar a imagem
            
            # Após salvar a imagem, redirecionar de volta para a tela anterior
            return redirect(url_for("paciente_dados"))
        
        # Se o método for GET, renderizar a tela de upload de imagem
        return render_template("upload-imagem.html", **components)
    
    @app.route("/overlay.html")
    def overlay():
        return render_template("overlay.html")

    @app.route("/static/<path:filename>")
    def static_files(filename):
        return send_from_directory("static", filename)
    