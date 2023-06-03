from flask import render_template, redirect, request, url_for, send_from_directory, Response, send_file
from flask_bcrypt import Bcrypt, check_password_hash
from .components import *
from pymongo import MongoClient
from gridfs import GridFS
from PIL import Image
from io import BytesIO
import cv2
import numpy as np

client = MongoClient('localhost', 27017)
db = client['clinica_0']
fs = GridFS(db)

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
        }

def init_app(app, bcrypt):

    @app.route("/", methods=['GET','POST'])
    def index():
        minify_css()
        if request.method == 'POST':
            username = request.form['user-login']
            user = db.Usuarios.find_one({'login': username})
            if user and check_password_hash(user['senha'], request.form['user-password']):
                return redirect(url_for('cadastro_monitor'))
            else:
                return 'Usuário ou senha invalido'
        return render_template("login.html")
    
    @app.route("/dashboard")
    def dashboard():
        return render_template("dashboard.html", **components)
    
    @app.route("/pacientes")
    def pacientes():
        return render_template("pacientes.html", **components)
    
    @app.route("/paciente-dados")
    def paciente_dados():
        return render_template("paciente-dados.html", **components)
      
    @app.route("/paciente-diagnostico")
    def paciente_diagnostico():
        return render_template("paciente-diagnostico.html", **components)
    
    @app.route("/paciente-familiar")
    def paciente_familiar():
        return render_template("paciente-familiar.html", **components)
    
    def rotate_image(image, angle):
        # Esta função recebe uma imagem e um ângulo como entrada e retorna uma nova imagem que é rotacionada pelo ângulo fornecido.

        # obter a altura e a largura da imagem
        height, width = image.shape[:2]
        # obter o ponto central da imagem
        center = (width / 2, height / 2)
        # obter a matriz de rotação
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        
        # calcular o tamanho da nova imagem para acomodar a imagem rotacionada inteira
        cos = np.abs(rotation_matrix[0, 0])
        sin = np.abs(rotation_matrix[0, 1])
        new_width = int((height * sin) + (width * cos))
        new_height = int((height * cos) + (width * sin))
        
        # ajustar a matriz de rotação para levar em conta o deslocamento
        rotation_matrix[0, 2] += (new_width / 2) - center[0]
        rotation_matrix[1, 2] += (new_height / 2) - center[1]
        
        # rotacionar a imagem
        rotated_image = cv2.warpAffine(image, rotation_matrix, (new_width, new_height), borderValue=(255, 255, 255))
        
        return rotated_image

    @app.route("/cadastro-monitor", methods=['GET', 'POST'])
    def cadastro_monitor():
        if request.method == 'POST':
            password = request.form['senha-monitor']
            password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
            monitor_login = {
                'login': request.form['login-monitor'],
                'senha': password_hash,
                'nivel': 'normal',
            }

            image_file = request.files['foto']
            image = cv2.imdecode(np.fromstring(image_file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
            angle = float(request.form['angle']) # obter o valor do ângulo de rotação do rotationRange

            imageR = rotate_image(image, -angle)

            _, png_image = cv2.imencode('.png', imageR)
            # enviar a imagem como uma resposta HTTP
            return Response(png_image.tostring(), mimetype='image/png')

        return render_template("cadastro-monitor.html", **components)
    
    @app.route("/cadastro-clinica")
    def cadastro_clinica():
        return render_template("cadastro-clinica.html", **components)
    
    @app.route("/upload-imagem", methods=["GET", "POST"])
    def upload_imagem():
        if request.method == "POST":
            # Salvar a imagem e fazer qualquer processamento necessário
            # Aqui, você pode usar bibliotecas como Pillow para rotacionar a imagem
            
            # Após salvar a imagem, redirecionar de volta para a tela anterior
            return redirect(url_for("paciente_dados"))
    
        # Se o método for GET, renderizar a tela de upload de imagem
        return render_template("upload-imagem.html")

    @app.route("/overlay.html")
    def overlay():
        return render_template("overlay.html")

    @app.route("/static/<path:filename>")
    def static_files(filename):
        return send_from_directory("static", filename)
    
    @app.route("/paciente")
    def paciente():
        return render_template("paciente.html", **components)
    
    @app.route("/consulta-pacientes")
    def consulta_pacientes():
        return render_template("consulta-pacientes.html", **components)
    
    @app.route("/consulta-monitores")
    def consulta_monitores():
        return render_template("consulta-monitores.html", **components)