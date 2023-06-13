# Tera
<aside><strong>Sistema de monitoramento pós-clínico de dependentes químicos reabilitados</strong></aside>

###### Descrição
<p>Este é um projeto de criação de um painel de controle (dashboard) utilizando as tecnologias Flask, MongoDB e ApexCharts. O objetivo do projeto é fornecer uma interface visual intuitiva para visualização e análise de dados armazenados em um banco de dados MongoDB, utilizando a estrutura de desenvolvimento web Flask e a biblioteca de gráficos ApexCharts.</p><br>

## Como rodar este projeto?

###### Requisitos

<li>Python</li>
<li>MongoDB</li>
<li>VSCode</li>

## Instalação

1. Clone o repositório para o seu computador:

```
git clone https://github.com/aasjunior/tera_dashboard.git
```

2. Abra o projeto pelo VSCode e execute o comando pelo terminal: 

```
pip install -r requirements.txt
```

3. Execute o projeto pelo comando:

```
py app.py
```

## Configurando a base de dados

1. Crie duas bases de dados no MongoDB: tera e clinica_0.
2. Dentro de cada base de dados, crie coleções com o mesmo nome dos arquivos listados abaixo.
3. Insira os documentos nas respectivas coleções.

A estrutura das bases de dados e coleções deve ser a seguinte:

### Base de dados [tera](models/base_dados/tera):

```
📁 tera
- 📄 Clinicas.json
- 📄 Usuarios.json
```

### Base de dados [clinica_0](models/base_dados/clinica_0):

```
📁 clinica_0
- 📄 Monitores.json
- 📄 Pacientes.json
- 📄 Familiares.json
- 📄 DadosMedicos.json
- 📄 DadosSensores.json
- 📄 RegistrosHumor.json
- 📄 fs.chunks.json
- 📄 fs.files.json
```

## Acessando o sistema

Para logar no sistema como administrador, utilize o usuário de Pedro:

```
Usuário: pedrodias
Senha: 1234
```
