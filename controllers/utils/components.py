from flask import render_template, session
from models.database import *
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from gridfs import GridFS
from gridfs.errors import NoFile
from bson.objectid import ObjectId
from base64 import b64encode

def imageDB():
    client = conn('localhost', 27017, session['clinica_db'])
    db = client.get_default_database()
    fs = GridFS(db)

    # obter o valor do campo fotoid da sessão
    image_id = session['fotoid']
    
    try:
        # consultar os dados da imagem no banco de dados
        image = fs.get(ObjectId(image_id))
        
        # ler os dados da imagem
        image_data = image.read()
        
        # codificar os dados da imagem em base64
        image_base64 = 'data:image/png;base64,' + b64encode(image_data).decode('utf-8')

        return image_base64
    except NoFile:
        # lidar com o caso em que a imagem não foi encontrada
        return None

def render_sidebar():
    image = imageDB() or 'user.png'
    return render_template("components/sidebar.html", image=image)

def render_welcome_card(name, pag=False, titulo=False):
    return render_template("components/welcome-card.html", name=name, pag=pag, titulo=titulo)

def render_upload_image(pag=False):
    return render_template("components/upload-image.html", pag=pag)
  
def render_monthly_record(mal, bom, sem_resposta):
    dados = {
        'mal': mal,
        'bom': bom,
        'sem_resposta': sem_resposta,
    }
    return render_template("components/monthly-record.html", **dados)

def render_header_title(titulo_da_pag=False):
    return render_template("components/header-title.html", titulo_da_pag=titulo_da_pag)

def render_progress_bar():
    return render_template("components/progress-bar.html")

def render_crisis_patient_card(paciente):
    return render_template("components/crisis-patient-card.html", paciente=paciente)

def render_offline_patient_card(paciente):
    return render_template("components/offline-patient-card.html", paciente=paciente)

components = {
            'sidebar': render_sidebar,
            'welcome_card': render_welcome_card,
            'monthly_record': render_monthly_record,
            'header_title' : render_header_title,
            'crisis_patient_card' : render_crisis_patient_card,
            'upload_image': render_upload_image,
            'header_title' : render_header_title,
            'progress_bar' : render_progress_bar,
            'offline_patient_card': render_offline_patient_card,
        }