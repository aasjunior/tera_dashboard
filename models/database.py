from flask import session
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

def create_monitor_login(bcrypt, form, clinica_db):
    password_hash = bcrypt.generate_password_hash(form['senha-monitor']).decode('utf-8')
    return {
        'login': form['login-monitor'],
        'senha': password_hash,
        'nivel': 'normal',
        'clinica_db': clinica_db,
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

def create_paciente_dados(image_id):
    return {
        'nome': session.get('paciente_dados', {}).get('nome-paciente', ''),
        'data_nascimento': session.get('paciente_dados', {}).get('data-nasc-paciente', ''),
        'cpf': session.get('paciente_dados', {}).get('cpf-paciente', ''),
        'rg': session.get('paciente_dados', {}).get('rg-paciente', ''),
        'celular': session.get('paciente_dados', {}).get('cel-paciente', ''),
        'email': session.get('paciente_dados', {}).get('email-paciente', ''),
        'endereco': [{
            'logradouro': session.get('paciente_dados', {}).get('endereco-paciente', ''),
            'numero': session.get('paciente_dados', {}).get('numero-endereco-paciente', ''),
            'cep': session.get('paciente_dados', {}).get('cep-paciente', ''),
            'cidade': session.get('paciente_dados', {}).get('cidade-paciente', ''),
            'uf': session.get('paciente_dados', {}).get('estado-paciente', '')
        }],
        'imagem_id': image_id,
    }

def create_familiar(image_id, paciente_id):
    return {
        'tipo_sanguineo': session.get('familiar', {}).get('sangue-familiar', ''),
        'parentesco': session.get('familar', {}).get('parentesco', ''),
        'nome': session.get('familiar', {}).get('nome-familiar', ''),
        'data_nascimento': session.get('familiar', {}).get('data-nasc-familiar', ''),
        'cpf': session.get('familiar', {}).get('cpf-familiar', ''),
        'rg': session.get('familiar', {}).get('rg-familiar', ''),
        'celular': session.get('familiar', {}).get('cel-familiar', ''),
        'email': session.get('familiar', {}).get('email-familiar', ''),
        'endereco': [{
            'logradouro': session.get('familiar', {}).get('endereco-familiar', ''),
            'numero': session.get('familiar', {}).get('numero-endereco-familiar', ''),
            'cep': session.get('familiar', {}).get('cep-familiar', ''),
            'cidade': session.get('familiar', {}).get('cidade-familiar', ''),
            'uf': session.get('familiar', {}).get('estado-familiar', '')
        }],
        'imagem_id': image_id,
        'paciente_id': paciente_id
    }

def create_dados_medicos(paciente_id):
    medicamento_list = []
    for lembrete in session.get('lembretes_medicamentos', []):
        hora_lembrete = lembrete[0]
        medicamento = lembrete[1]
        medicamento_list.append({
            'nome': medicamento,
            'hora': hora_lembrete
        })
    return {
        'tipo_sanguineo': session.get('paciente_dados', {}).get('sangue-paciente', ''),
        'altura': session.get('paciente_dados', {}).get('altura-paciente', ''),
        'peso': session.get('paciente_dados', {}).get('peso-paciente', ''),
        'titulo-diagnostico': session.get('dados_medicos', {}).get('diagnostico-paciente', ''),
        'descricao-diagnostico': session.get('dados_medicos', {}).get('descricao-diagnostico', ''),
        'admissao': session.get('dados_medicos', {}).get('data-admissao', ''),
        'alta': session.get('dados_medicos', {}).get('data-alta', ''),
        'medicamento': medicamento_list,
        'paciente_id': paciente_id,
    }