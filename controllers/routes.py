from flask import render_template
from .components import *

def init_app(app):

    @app.route("/")
    def index():
        components = {
            'sidebar': render_sidebar,
            'welcome_card': render_welcome_card,
        }
        return render_template("index.html", **components)