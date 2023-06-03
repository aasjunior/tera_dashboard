from flask import render_template
from .components import *
from PIL import Image

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

def render_monthly_record(mal, bom, sem_resposta):
    dados = {
        'mal': mal,
        'bom': bom,
        'sem_resposta': sem_resposta,
    }
    return render_template("components/monthly-record.html", **dados)

def render_header_title(titulo_da_pag=False):
    return render_template("components/header-title.html", titulo_da_pag=titulo_da_pag)

def rotate_image(image_path, degrees):
    image = Image.open(image_path)
    rotated_image = image.rotate(degrees, expand=True)
    rotated_image.save(image_path)

def render_progress_bar():
    return render_template("components/progress-bar.html")

def render_crisis_patient_card():
    return render_template("components/crisis-patient-card.html")

def render_offline_patient_card():
    return render_template("components/offline-patient-card.html")

components = {
            'sidebar': render_sidebar,
            'welcome_card': render_welcome_card,
            'daily_record': render_daily_record,
            'annual_record': render_annual_record,
            'monthly_record': render_monthly_record,
            'header_title' : render_header_title,
            'crisis_patient_card' : render_crisis_patient_card,
            'upload_image': render_upload_image,
            'header_title' : render_header_title,
            'progress_bar' : render_progress_bar,
            'offline_patient_card': render_offline_patient_card,
        }