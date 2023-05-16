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

def render_daily_record(name):
    return render_template("components/daily-record.html", name=name)
