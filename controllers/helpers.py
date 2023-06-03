from flask import render_template, redirect, request, url_for, send_from_directory, Response, send_file
from flask_bcrypt import Bcrypt, check_password_hash
from pymongo import MongoClient
from gridfs import GridFS
from cv2 import imdecode, IMREAD_UNCHANGED, getRotationMatrix2D, warpAffine, imencode, cvtColor, COLOR_RGB2RGBA
from numpy import *
from cssmin import cssmin
from uuid import *
from datetime import datetime

def minify_css():
    css_files = [
        'views/static/css/global.css',
        'views/static/css/custom.css',
        'views/static/css/charts.css',
        'views/static/css/dados-paciente.css',
        'views/static/css/diagnostico-paciente.css',
        'views/static/css/login.css',
        'views/static/css/pacientes-dash.css',
        'views/static/css/progress-bar.css',
        'views/static/css/responsive.css'
    ]
    combined_css = ''

    for file in css_files:
        with open(file, 'r') as f:
            css_content = f.read()
            combined_css += css_content


    minified_css = cssmin(combined_css)
    
    output_file = 'views/static/css/styles.min.css'

    with open(output_file, 'w') as f:
        f.write(minified_css)

## Rotação imagem
# Esta função recebe uma imagem e um ângulo como entrada e retorna uma nova imagem que é rotacionada pelo ângulo fornecido.
def rotate_image(image, angle):
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

def encode_image(image_file, angle):
    image = imdecode(fromstring(image_file.read(), uint8), IMREAD_UNCHANGED)
    if angle != 0:
        rotated_image = rotate_image(image, -angle)
        
        # A função imencode retorna uma tupla com dois valores, '_' indica é uma convensão em python para ignorar o primeiro valor (valor que indica se a codificação foi bem sucedida), enquanto o segundo valor é atribuido a variavel encoded_image
        _, encoded_image = imencode('.png', rotated_image)
    else:
        _, encoded_image = imencode('.png', image)
    return encoded_image

def generate_unique_filename(extension):
    # gerar um UUID usando o algoritmo MD5
    unique_id = uuid4()
    # converter o UUID em uma string hexadecimal
    unique_name = unique_id.hex
    # adicionar a extensão do arquivo de imagem ao nome único
    filename = unique_name + '.' + extension
    return filename

## CRUD

def create_monitor_login(bcrypt, form):
    password_hash = bcrypt.generate_password_hash(form['senha-monitor']).decode('utf-8')
    return {
        'login': form['login-monitor'],
        'senha': password_hash,
        'nivel': 'normal',
        'data_cadastro': datetime.now()
    }

def create_monitor_dados(form, image_id, user_id):
    return {
        'nome': form['nome-monitor'],
        'data-nascimento': form['data-nasc-monitor'],
        'cpf': form['cpf-monitor'],
        'rg': form['rg-monitor'],
        'celular': form['cel-monitor'],
        'email': form['email-monitor'],
        'endereco': [{
            'logradouro': form['endereco-monitor'],
            'numero': form['numero-endereco-monitor'],
            'cep': form['cep-monitor'],
            'cidade': form['cidade-monitor'],
            'uf': form['estado-monitor']
        }],
        'imagem_id': image_id,
        'usuario_id': user_id
    }
