from flask import render_template, redirect, request, url_for, send_from_directory, Response, send_file
from flask_bcrypt import Bcrypt, check_password_hash
from .components import *
from pymongo import MongoClient
from gridfs import GridFS
from PIL import Image
from io import BytesIO
from cv2 import *
from cv2 import imdecode, IMREAD_UNCHANGED, getRotationMatrix2D, warpAffine, imencode, cvtColor, COLOR_RGB2RGBA
from numpy import *
from uuid import *
from datetime import datetime

client = MongoClient('localhost', 27017)
db = client['clinica_0']
fs = GridFS(db)

def rotate_image(image, angle):
    # Esta função recebe uma imagem e um ângulo como entrada e retorna uma nova imagem que é rotacionada pelo ângulo fornecido.

    # verificar se a imagem tem 3 canais (RGB)
    if len(image.shape) == 3 and image.shape[2] == 3:
    # converter a imagem para RGBA
        image = cvtColor(image, COLOR_RGB2RGBA)

    # obter a altura e a largura da imagem
    height, width = image.shape[:2]
    # obter o ponto central da imagem
    center = (width / 2, height / 2)
    # obter a matriz de rotação
    rotation_matrix = getRotationMatrix2D(center, angle, 1.0)
    
    # calcular o tamanho da nova imagem para acomodar a imagem rotacionada inteira
    cos = abs(rotation_matrix[0, 0])
    sin = abs(rotation_matrix[0, 1])
    new_width = int((height * sin) + (width * cos))
    new_height = int((height * cos) + (width * sin))
    
    # ajustar a matriz de rotação para levar em conta o deslocamento
    rotation_matrix[0, 2] += (new_width / 2) - center[0]
    rotation_matrix[1, 2] += (new_height / 2) - center[1]
    
    # rotacionar a imagem
    rotated_image = warpAffine(image, rotation_matrix, (new_width, new_height), borderValue=(0, 0, 0, 0))
    
    return rotated_image

def generate_unique_filename(extension):
    # gerar um UUID usando o algoritmo MD5
    unique_id = uuid4()
    # converter o UUID em uma string hexadecimal
    unique_name = unique_id.hex
    # adicionar a extensão do arquivo de imagem ao nome único
    filename = unique_name + '.' + extension
    return filename

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

    @app.route("/cadastro-monitor", methods=['GET', 'POST'])
    def cadastro_monitor():
        if request.method == 'POST':
            password = request.form['senha-monitor']
            password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
            monitor_login = {
                'login': request.form['login-monitor'],
                'senha': password_hash,
                'nivel': 'normal',
                'data_cadastro': datetime.now()
            }

            image_file = request.files['foto']
            image = imdecode(fromstring(image_file.read(), uint8), IMREAD_UNCHANGED)
            angle = float(request.form['angle']) # obter o valor do ângulo de rotação do rotationRange

            if angle != 0:
                rotated_image = rotate_image(image, -angle)
            
                # A função imencode retorna uma tupla com dois valores, 
                # '_' indica é uma convensão em python para ignorar o primeiro valor (valor que indica se a codificação foi bem sucedida), 
                # enquanto o segundo valor é atribuido a variavel encoded_image
                _, encoded_image = imencode('.png', rotated_image)
            else:
                _, encoded_image = imencode('.png', image)

            # gerar um nome de arquivo único para a imagem rotacionada
            image_filename = generate_unique_filename('png')

            # salvar a imagem rotacionada no MongoDB usando GridFS
            image_id = fs.put(encoded_image.tostring(), filename=image_filename)

            user = db.Usuarios.insert_one(monitor_login)
            user_id = user.inserted_id
            
            monitor_dados = {
                'nome': request.form['nome-monitor'],
                'data-nascimento': request.form['data-nasc-monitor'],
                'cpf': request.form['cpf-monitor'],
                'rg': request.form['rg-monitor'],
                'celular': request.form['cel-monitor'],
                'email': request.form['email-monitor'],
                'endereco': [
                    {
                        'logradouro': request.form['endereco-monitor'],
                        'numero': request.form['numero-endereco-monitor'],
                        'cep': request.form['cep-monitor'],
                        'cidade': request.form['cidade-monitor'],
                        'uf': request.form['estado-monitor']
                    }
                ],
                'imagem_id': image_id,
                'usuario_id': user_id
            }

            db.Monitores.insert_one(monitor_dados)
            image_data = fs.get(image_id).read()

            # enviar a imagem como uma resposta HTTP
            return Response(image_data, mimetype='image/png')

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