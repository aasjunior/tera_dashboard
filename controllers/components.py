from flask import render_template
from .components import *

def render_sidebar(name, image):
    user = {
        'name': name,
        'image': image,
    }

    return render_template("components/sidebar.html", **user)

def render_welcome_card(name, fig=False):
    return render_template("components/welcome-card.html", name=name, fig=fig)

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
