from flask import render_template
from .components import *

def render_sidebar(name, image):
    user = {
        'name': name,
        'image': image,
    }
    return render_template("components/sidebar.html", **user)

def render_welcome_card(name, pag=False, titulo=False):
    return render_template("components/welcome-card.html", name=name, pag=pag, titulo=titulo)

def render_upload_image(pag=False):
    return render_template("components/upload-image.html", pag=pag)
  
def render_daily_record(mal, bom, sem_resposta):
    dados = {
        'mal': mal,
        'bom': bom,
        'sem_resposta': sem_resposta,
    }
    return render_template("components/daily-record.html", **dados)

def render_annual_record(mal, bom, sem_resposta):
    dados = {
        'mal': mal,
        'bom': bom,
        'sem_resposta': sem_resposta,
    }
    return render_template("components/annual-record.html", **dados)

def render_header_title(titulo_da_pag=False):
    return render_template("components/header-title.html", titulo_da_pag=titulo_da_pag)

def render_progress_bar():
    return render_template("components/progress-bar.html")

def render_crisis_patient_card():
    return render_template("components/crisis-patient-card.html")

def render_offline_patient_card():
    return render_template("components/offline-patient-card.html")
