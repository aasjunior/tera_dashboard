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

def render_daily_record(name):
    return render_template("components/daily-record.html", name=name)

def render_header_title(titulo_da_pag=False):
    return render_template("components/header-title.html", titulo_da_pag=titulo_da_pag)

def render_progress_bar():
    return render_template("components/progress-bar.html")
