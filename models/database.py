from flask_bcrypt import Bcrypt, check_password_hash
from pymongo import MongoClient
from gridfs import GridFS
from datetime import datetime

def conn(host, port, db_name, username = None, password = None):
    if username and password:
        uri = f'mongodb://{username}:{password}@{host}:{port}/{db_name}'
    else:
        uri = f'mongodb://{host}:{port}/{db_name}'
    client = MongoClient(uri)
    return client

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
