from flask import Flask, render_template, request
from pymongo import MongoClient
import math

client = MongoClient('localhost', 27017)

app = Flask(__name__)

# Acessa a coleção 'dados' no banco de dados 'monitor'
db = client['monitor']
collection = db['dados']

@app.route('/')
def index():
    total_registros = collection.count_documents({})
    num_paginas = math.ceil(total_registros / 10)  # Calcula o número total de páginas

    # Obtém os registros da página atual
    page_num = request.args.get('page', default=1, type=int)
    skip_num = (page_num - 1) * 10
    registros = list(collection.find().sort('_id', -1).skip(skip_num).limit(10))

    # Renderiza o template HTML passando os registros e informações de paginação
    return render_template('pag-1.html', registros=registros, num_paginas=num_paginas, page_num=page_num)


@app.route('/pagina/<int:page_num>')
def pagina(page_num=1):
    total_registros = collection.count_documents({})
    num_paginas = math.ceil(total_registros / 10)  # Calcula o número total de páginas

    skip_num = (page_num - 1) * 10
    registros = list(collection.find().sort('_id', -1).skip(skip_num).limit(10))

    return render_template('pag-1.html', registros=registros, num_paginas=num_paginas, page_num=page_num)



if __name__ == "__main__":
    app.run(debug=True)
