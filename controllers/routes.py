from flask import render_template
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