from flask import session
from pymongo import MongoClient
from gridfs import GridFS
from datetime import datetime, timedelta
import pandas as pd
import random

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
        'data_cadastro': datetime.now()
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

def consultar_registros(db):
    # Data e hora atuais
    agora = datetime.now()

    # Data e hora de 24 horas atrás
    ultimas_24_horas = agora - timedelta(days=1)

    # Converter datas e horas para strings
    agora_str = agora.strftime("%Y-%m-%d %H:%M:%S.%f")
    ultimas_24_horas_str = ultimas_24_horas.strftime("%Y-%m-%d %H:%M:%S.%f")

    # Consultar registros de humor nas últimas 24 horas
    registros = db.RegistrosHumor.aggregate([
        {
            "$match": {
                "data_registro": {"$gte": ultimas_24_horas_str, "$lte": agora_str}
            }
        },
        {
            "$group": {
                "_id": "$paciente_id",
                "registros": {"$push": "$humor"}
            }
        }
    ])

    # Inicializar contadores
    registros_bom = 0
    registros_mal = 0
    pacientes_com_resposta = set()

    # Contar registros de humor
    for registro in registros:
        for humor in registro["registros"]:
            if humor == "Bom":
                registros_bom += 1
            elif humor == "Mal":
                registros_mal += 1

        pacientes_com_resposta.add(str(registro["_id"]))

    total_respostas = registros_bom + registros_mal
    # Contagem de pacientes sem registro nas últimas 24 horas
    total_pacientes = db.Pacientes.count_documents({})
    pacientes_sem_resposta = total_pacientes - len(pacientes_com_resposta)

    return {
        "registros_bom": registros_bom,
        "registros_mal": registros_mal,
        "registros_sem_resposta": pacientes_sem_resposta,
        "total_pacientes": total_pacientes,
        "ultimas_24_horas": ultimas_24_horas,
        "agora": agora,
        "total_respostas": total_respostas
    }

def consultar_registros_anual(db):
    # Data e hora atuais
    agora = datetime.now()

    # Contar registros de humor para o dia atual
    total_pacientes = db.Pacientes.count_documents({})
    humor_bom = db.RegistrosHumor.count_documents({"humor": "Bom", "data_registro": {"$gte": agora.replace(hour=0, minute=0, second=0), "$lte": agora.replace(hour=23, minute=59, second=59)}})
    humor_mal = db.RegistrosHumor.count_documents({"humor": "Mal", "data_registro": {"$gte": agora.replace(hour=0, minute=0, second=0), "$lte": agora.replace(hour=23, minute=59, second=59)}})
    sem_resposta = total_pacientes - (humor_bom + humor_mal)

    # Inicializar contadores
    data_mal = [0] * 12
    data_bom = [0] * 12
    data_sem_resposta = [0] * 12

    # Contar registros de humor para cada mês do ano
    for mes in range(1, 13):
        inicio_mes = datetime(agora.year, mes, 1)
        fim_mes = datetime(agora.year + (mes // 12), (mes % 12) + 1, 1)
        total_pacientes = db.Pacientes.count_documents({})
        humor_bom = db.RegistrosHumor.count_documents({"humor": "Bom", "data_registro": {"$gte": inicio_mes, "$lte": fim_mes}})
        humor_mal = db.RegistrosHumor.count_documents({"humor": "Mal", "data_registro": {"$gte": inicio_mes, "$lte": fim_mes}})
        sem_resposta = total_pacientes - (humor_bom + humor_mal)
        data_mal[mes - 1] = humor_mal
        data_bom[mes - 1] = humor_bom
        data_sem_resposta[mes - 1] = sem_resposta
        
    return {
        "data_mal": data_mal,
        "data_bom": data_bom,
        "data_sem_resposta": data_sem_resposta
    }

# Criar uma função para consultar os registros de humor dentro de um mês
def consultar_registros_mensal(db):
    # Data e hora atuais
    agora = datetime.now()

    # Inicializar contadores
    data_mal = []
    data_bom = []
    data_sem_resposta = []

    # Contar registros de humor para cada semana dentro do mês
    inicio_mes = datetime(agora.year, agora.month, 1)
    fim_mes = datetime(agora.year + (agora.month // 12), (agora.month % 12) + 1, 1)

    semanas_mes = pd.date_range(start=inicio_mes, end=fim_mes, freq='W')

    for semana in semanas_mes:
        inicio_semana = semana
        fim_semana = semana + pd.DateOffset(days=6)

        total_pacientes = db.Pacientes.count_documents({})
        humor_bom = db.RegistrosHumor.count_documents({"humor": "Bom", "data_registro": {"$gte": inicio_semana, "$lte": fim_semana}})
        humor_mal = db.RegistrosHumor.count_documents({"humor": "Mal", "data_registro": {"$gte": inicio_semana, "$lte": fim_semana}})
        sem_resposta = total_pacientes - (humor_bom + humor_mal)

        data_mal.append(humor_mal)
        data_bom.append(humor_bom)
        data_sem_resposta.append(sem_resposta)

    return {
        "data_mal": data_mal,
        "data_bom": data_bom,
        "data_sem_resposta": data_sem_resposta
    }


def panelCrisis(db):
    # Data e hora atuais
    agora = datetime.now()

    # Data e hora de 7 dias atrás
    ultimos_7_dias = agora - timedelta(days=7)

    # Converter datas e horas para strings
    agora_str = agora.strftime("%Y-%m-%d %H:%M:%S.%f")
    ultimos_7_dias_str = ultimos_7_dias.strftime("%Y-%m-%d %H:%M:%S.%f")

      # Consultar registros de humor nos últimos 7 dias
    registros = db.RegistrosHumor.aggregate([
        {
            "$match": {
                "data_registro": {"$gte": ultimos_7_dias_str, "$lte": agora_str},
                "humor": {"$in": ["Mal", "Bom"]}
            }
        },
        {
            "$group": {
                "_id": "$paciente_id",
                "registros": {"$push": "$humor"}
            }
        }
    ])

    pacientes_em_crise = set()
    crises_resolvidas = 0
    total_registros_mal = 0

    # Verificar pacientes em crise e crises resolvidas
    for registro in registros:
        paciente_id = str(registro["_id"])  # Converter para string
        registros_paciente = registro["registros"]
        if "Mal" in registros_paciente:
            pacientes_em_crise.add(paciente_id)
            if "Bom" in registros_paciente:
                crises_resolvidas += 1
        total_registros_mal += registros_paciente.count("Mal")

    total_pacientes_em_crise = len(pacientes_em_crise)

    # Obter os primeiros 5 pacientes em crise
    pacientes_em_crise = list(pacientes_em_crise)[:5]

    return {
        "pacientes_em_crise": pacientes_em_crise,
        "crises_resolvidas": crises_resolvidas,
        "total_pacientes_em_crise": total_pacientes_em_crise,
        "total_registros_mal": total_registros_mal
    }

def pacientesNovos(db):
    # Data de hoje
    data_atual = datetime.now()

    # Data da semana anterior
    data_semana_anterior = data_atual - timedelta(days=7)

    # Consulta no banco de dados para obter a quantidade de pacientes cadastrados na semana
    total_pacientes = db.Pacientes.count_documents({
        "data_cadastro": {
            "$gte": data_semana_anterior,
            "$lt": data_atual
        }
    })

    return {
        "pacientes_novos": total_pacientes,
    }

def create_registro_humor(db, paciente_id):
    # Documento modelo
    documento_modelo = {
        "humor": "",
        "paciente_id": {
            "$oid": paciente_id
        },
        "data_registro": ""
    }

    # Data e hora atuais
    agora = datetime.now()

    # Gerar valor aleatório entre "Bom" e "Mal"
    documento = documento_modelo.copy()
    documento["humor"] = random.choice(["Bom", "Mal"])
    documento["data_registro"] = agora.strftime("%Y-%m-%d %H:%M:%S.%f")
    db.RegistrosHumor.insert_one(documento)

    # # Criar 12 documentos para os últimos 12 meses
    # for i in range(1, 13):
    #     data_registro = agora.replace(month=i, day=1, hour=0, minute=0, second=0, microsecond=0)
    #     documento = documento_modelo.copy()
    #     # Gerar valor aleatório entre "Bom" e "Mal"
    #     documento["humor"] = random.choice(["Bom", "Mal"])
    #     documento["data_registro"] = data_registro.strftime("%Y-%m-%d %H:%M:%S.%f")
    #     db.RegistrosHumor.insert_one(documento)

def create_dados_sensores(db, paciente_id):
    agora = datetime.now()
    data = {
        "paciente_id": paciente_id,
        "passos_percorridos": str(random.randint(0, 10000)),
        "bpms": str(random.randint(60, 100)),
        "start_time": datetime.strptime("2023-05-23T22:00:00Z", '%Y-%m-%dT%H:%M:%SZ'),
        "end_time": datetime.strptime("2023-05-24T06:00:00Z", '%Y-%m-%dT%H:%M:%SZ'),
        "duration_minutes": 480,
        "sleep_quality": "good",
        "data_registro": agora
    }
    db.DadosSensores.insert_one(data)