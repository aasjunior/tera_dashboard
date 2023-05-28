from flask import render_template
from .components import *
from PIL import Image
from cssmin import cssmin
from glob import glob
from os import listdir, path

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

def minify_css():
    css_files = [
        'views/static/css/global.css',
        'views/static/css/custom.css',
        'views/static/css/charts.css',
        'views/static/css/dados-paciente.css',
        'views/static/css/diagnostico-paciente.css',
        'views/static/css/login.css',
        'views/static/css/pacientes-dash.css',
        'views/static/css/progress-bar.css',
        'views/static/css/responsive.css'
    ]
    combined_css = ''

    for file in css_files:
        with open(file, 'r') as f:
            css_content = f.read()
            combined_css += css_content


    minified_css = cssmin(combined_css)
    
    output_file = 'views/static/css/styles.min.css'

    with open(output_file, 'w') as f:
        f.write(minified_css)