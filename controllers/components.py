from flask import render_template

def render_sidebar(name, image):
    user = {
        'name': name,
        'image': image,
    }

    return render_template("components/sidebar.html", **user)
