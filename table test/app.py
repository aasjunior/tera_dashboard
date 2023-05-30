from flask import Flask, render_template
from pymongo import MongoClient

client = MongoClient('localhost', 27017)

app = Flask(__name__)

@app.route('/')
def index():
    # Acessa a coleção 'dados' no banco de dados 'monitor'
    db = client['monitor']
    collection = db['dados']
    
    # Obtém os últimos 10 registros em ordem decrescente
    registros = collection.find().sort('_id', -1).limit(10)
    
    # Renderiza o template HTML passando os registros para exibição na tabela
    return render_template('pag-1.html', registros=registros)

@app.route('/pagina2')
def pagina2():
    # Acessa a coleção 'dados' no banco de dados 'monitor'
    db = client['monitor']
    collection = db['dados']
    
    # Obtém os registros anteriores aos 10 mais recentes em ordem decrescente
    registros = collection.find().sort('_id', -1).skip(10)
    
    # Renderiza o template HTML passando os registros para exibição na tabela
    return render_template('pag-2.html', registros=registros)

if __name__ == "__main__":
    app.run(debug=True)
