from flask import Flask
from controllers import routes
from controllers.utils import helpers
from flask_bcrypt import Bcrypt

app = Flask(__name__, template_folder="views", static_folder="views/static")
app.secret_key = '1234'
app.config['UPLOAD_FOLDER'] = "views/static/tmp"
bcrypt = Bcrypt(app)
helpers.minify_css()
routes.init_app(app, bcrypt)

if __name__ == "__main__":
    app.run(debug=True)