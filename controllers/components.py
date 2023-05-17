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

def render_daily_record(name):
    return render_template("components/daily-record.html", name=name)

def rotate_image(image_path, degrees):
    image = Image.open(image_path)
    rotated_image = image.rotate(degrees, expand=True)
    rotated_image.save(image_path)