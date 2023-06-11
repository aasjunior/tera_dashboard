from flask import session
from pymongo import MongoClient
from gridfs import GridFS
from bson.objectid import ObjectId
from bson.codec_options import CodecOptions
from base64 import b64encode
from datetime import datetime, timedelta, date
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
        'observacao': session.get('paciente_dados', {}).get('obs-paciente', ''),
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
        "paciente_id": paciente_id,
        "data_registro": "",
        "calorias_queimadas": 0
    }

    # Data e hora atuais
    agora = datetime.now()

    # Gerar valor aleatório entre "Bom" e "Mal"
    documento = documento_modelo.copy()
    documento["humor"] = random.choice(["Bom", "Mal"])
    documento["data_registro"] = agora.strftime("%Y-%m-%d %H:%M:%S.%f")
    documento["calorias_queimadas"] = random.randint(0, 1000)
    db.RegistrosHumor.insert_one(documento)

    # Criar 12 documentos para os últimos 12 meses
    for i in range(1, 13):
        # Calcular a data para o ano anterior
        data_registro = agora - timedelta(days=365)
        data_registro = data_registro.replace(month=i, day=1, hour=0, minute=0, second=0, microsecond=0)
        
        documento = documento_modelo.copy()
        # Gerar valor aleatório entre "Bom" e "Mal"
        documento["humor"] = random.choice(["Bom", "Mal"])
        documento["data_registro"] = data_registro.strftime("%Y-%m-%d %H:%M:%S.%f")
        db.RegistrosHumor.insert_one(documento)

def create_dados_sensores(db, paciente_id):
    agora = datetime.now()
    
    # Gerar hora de início do sono aleatória entre 20:00 e 23:00
    hora_inicio_sono = random.randint(20, 23)
    minuto_inicio_sono = random.randint(0, 59)
    start_time = agora.replace(hour=hora_inicio_sono, minute=minuto_inicio_sono, second=0, microsecond=0)
    start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Gerar duração do sono aleatória entre 6 e 9 horas
    duracao_sono_horas = random.randint(6, 9)
    duracao_sono_minutos = duracao_sono_horas * 60
    
    # Calcular hora de término do sono
    end_time = start_time + timedelta(minutes=duracao_sono_minutos)
    end_time_str = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    data = {
        "paciente_id": paciente_id,
        "passos_percorridos": str(random.randint(0, 10000)),
        "bpms": str(random.randint(60, 100)),
        "start_time": datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M:%SZ'),
        "end_time": datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M:%SZ'),
        "duration_minutes": duracao_sono_minutos,
        "sleep_quality": "good",
        "data_registro": agora
    }
    db.DadosSensores.insert_one(data)

def pacientes_sem_registro_humor(db):
    fs = GridFS(db)
    # Obter a data atual e a data de um dia atrás
    data_atual = datetime.now()
    data_um_dia_atras = data_atual - timedelta(days=1)

    # Criar índice na coleção Pacientes
    db.Pacientes.create_index("_id")

    # Criar índice na coleção RegistrosHumor
    db.RegistrosHumor.create_index("data_registro")

    # Consultar os registros de humor nos últimos dias
    registros_humor = list(db.RegistrosHumor.find({
        'data_registro': {
            '$gte': data_um_dia_atras,
            '$lte': data_atual
        }
    }))

    # Obter os IDs dos pacientes que fizeram registro de humor nos últimos dias
    pacientes_com_registro_humor_ids = [registro['paciente_id']['$oid'] for registro in registros_humor]

    # Consultar os pacientes que não fizeram registro de humor nos últimos dias e estão offline há 1 ou mais dias
    pacientes_sem_registro_humor = list(db.Pacientes.find({
        '_id': {
            '$nin': pacientes_com_registro_humor_ids
        },
        'data_cadastro': {
            '$lte': data_um_dia_atras
        }
    }))

    # Obter os IDs dos pacientes sem registro de humor
    pacientes_sem_registro_humor_ids = [paciente['_id'] for paciente in pacientes_sem_registro_humor]

    # Consultar os registros de humor dos pacientes sem registro
    registros_humor_pacientes_sem_registro = list(db.RegistrosHumor.find({
        'paciente_id': {
            '$in': pacientes_sem_registro_humor_ids
        }
    }))

    # Obter os dados relacionados aos pacientes sem registro de humor
    dados_pacientes = []
    for paciente in pacientes_sem_registro_humor:
        paciente_id = paciente['_id']
        registro_humor = next((registro for registro in registros_humor_pacientes_sem_registro if registro['paciente_id'] == paciente_id), None)
        ultima_data_registro = datetime.strptime(registro_humor['data_registro'], "%Y-%m-%d %H:%M:%S.%f") if registro_humor else None
        if ultima_data_registro:
            quantidade_dias = (data_atual - ultima_data_registro).days
        else:
            data_cadastro = paciente['data_cadastro']
            quantidade_dias = (data_atual - data_cadastro).days

        image = fs.get(ObjectId(paciente['imagem_id']))
        image_data = image.read()
        image_base64 = 'data:image/png;base64,' + b64encode(image_data).decode('utf-8')

        dados = {
            'paciente': paciente,
            'dados_sensores': db.DadosSensores.find_one({'paciente_id': paciente_id}),
            'dados_medicos': db.DadosMedicos.find_one({'paciente_id': paciente_id}),
            'ultima_data_registro': ultima_data_registro,
            'quantidade_dias': quantidade_dias,
            'foto': image_base64,
            'registro_humor': registro_humor
        }
        dados_pacientes.append(dados)

    # Retornar o dicionário com os registros de humor e dados dos pacientes
    return {
        'registros_humor': registros_humor,
        'dados_pacientes': dados_pacientes
    }

def patient_dash_data(dados_sensores, dados_medicos):
    horas_sono = float(dados_sensores['duration_minutes']) / 60
    percentual_sono = (horas_sono / 8) * 100

    # Calcular IMC
    peso = float(dados_medicos['peso'])
    altura = float(dados_medicos['altura']) / 100
    imc =  peso / (altura ** 2)

    # Atribuir pontuação para IMC
    if imc < 18.5:
        pontuacao_imc = 0
    elif imc >= 18.5 and imc < 25:
        pontuacao_imc = 1
    else:
        pontuacao_imc = 0

    # Atribuir pontuação para horas de sono
    horas_adequadas_sono = 8
    if horas_sono >= horas_adequadas_sono:
        pontuacao_sono = 1
    else:
        pontuacao_sono = horas_sono / horas_adequadas_sono

    # Atribuir pontuação para passos percorridos
    passos_adequados = 10000
    if float(dados_sensores['passos_percorridos']) >= passos_adequados:
        pontuacao_passos = 1
    else:
        pontuacao_passos = float(dados_sensores['passos_percorridos']) / passos_adequados

    # Atribuir pontuação para BPMs
    if float(dados_sensores['bpms']) >= 60 and float(dados_sensores['bpms']) <= 100:
        pontuacao_bpms = 1
    else:
        pontuacao_bpms = 0

    # Calcular pontuação geral de saúde (média simples)
    pontuacao_geral = (pontuacao_imc + pontuacao_sono + pontuacao_passos + pontuacao_bpms) / 4

    # Converter pontuação geral em percentual
    percentual_saude = pontuacao_geral * 100

    horas_sono = dados_sensores['duration_minutes'] // 60
    minutos_sono = dados_sensores['duration_minutes'] % 60

    return{
        'horas_sono': horas_sono,
        'minutos_sono': minutos_sono,
        'percentual_sono': round(percentual_sono),
        'percentual_saude': round(percentual_saude)
    }

def registros_humor_individual(db, id):
    paciente_id = ObjectId(id)
    registros = db.RegistrosHumor.find({"paciente_id": paciente_id})

    # Contar o número de respostas "Mal" e "Bom"
    total_respostas = 0
    respostas_mal = 0
    respostas_bom = 0
    for registro in registros:
        total_respostas += 1
        if registro["humor"] == "Mal":
            respostas_mal += 1
        elif registro["humor"] == "Bom":
            respostas_bom += 1

    # Calcular o percentual de respostas "Mal" e "Bom"
    if total_respostas > 0:
        percentual_mal = round((respostas_mal / total_respostas) * 100)
        percentual_bom = round((respostas_bom / total_respostas) * 100)
    else:
        percentual_mal = 0
        percentual_bom = 0

    return{
        'percentual_bom': percentual_bom,
        'percentual_mal': percentual_mal
    }

def calcular_idade(dt_nascimento):
    data_nascimento_str = "1998-10-28"
    data_nascimento = date.fromisoformat(data_nascimento_str)
    hoje = date.today()
    idade = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))

    return idade