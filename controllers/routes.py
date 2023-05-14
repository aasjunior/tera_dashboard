from flask import render_template
from .components import render_sidebar

def init_app(app):

    @app.route("/")
    def index():
        components = {
            'sidebar': render_sidebar,
        }
        return render_template("index.html", **components)