<p align="center">
  <img src="https://github.com/aasjunior/tera_dashboard/assets/85968113/577ba1b6-3c9b-4b6b-9d3a-212c0e62d317" width="200" alt="logo">
</p>

# Tera 

<aside>Tera é um sistema de monitoramento pós-clínico de dependentes químicos reabilitados. Nosso objetivo é fornecer mais suporte ao paciente após sua alta e fortalecer a conexão entre Monitor clínico, Paciente e Família!<br /> </aside>

<div> <br> Nós começamos pelo Dashboard destinado ao uso dos Monitores de clínicas de reabilitação, onde é possível visualizar a condição dos pacientes sob seus cuidados, pacientes em crise ou que precisam de atenção redobrada e verificar os dados sobre um único paciente. </div>

### Os protótipos do Dashboard Tera:
<p align="center">
  <img src="https://github.com/aasjunior/tera_dashboard/assets/85968113/36193bc5-35b8-44be-95be-e4f948ee7374" width="700" alt="gif home">
  <img src="https://github.com/aasjunior/tera_dashboard/assets/85968113/ddff3e6d-7998-43eb-88df-1b5bee0b2f7b" width="700" height="" alt="imagens interfaces">
</p>

<div> <br> <strong> Mas como monitoramos o paciente? </strong> Esse processo deve ser voluntário, ao receber alta, o paciente receberá a oferta da clínica de usar um SmartWatch para o acompanhamento diário de sua condição mental e física. Já a família, poderá acompanhar o processo de seu celular, com um aplicativo móvel com funções como: lembrete de medicamentos do paciente, comunicação direta com o Monitor e atualizações do estado de seu ente querido. </div>

### Os protótipos do SmartWatch e App:
<p align="center">
  <img src="https://github.com/aasjunior/tera_dashboard/assets/85968113/c05711c1-2532-49e3-838e-f7c7fea92707" width="200" >
  <img src="https://github.com/aasjunior/tera_dashboard/assets/85968113/d581d467-087d-4f3c-b160-b702e9375082" width="200" >
  <img src="https://github.com/aasjunior/tera_dashboard/assets/85968113/3a821c96-6301-4870-a23e-3165c09a6190" width="200" >
</p>

<p align="center">
  <img src="https://github.com/aasjunior/tera_dashboard/assets/85968113/b7deac76-7627-4554-886c-64bc22671063" width="700" alt="gif home">
</p>

### Publicação de Artigo
Essa iniciativa foi publicada com sucesso na FECIVALE 2023 - Registro/SP (Instituto Federal - IF). [em breve atualizações]

## Como rodar este projeto?

###### Descrição
<p>Este é um projeto de criação de um painel de controle (dashboard) utilizando as tecnologias Flask, MongoDB e ApexCharts. O objetivo do projeto é fornecer uma interface visual intuitiva para visualização e análise de dados armazenados em um banco de dados MongoDB, utilizando a estrutura de desenvolvimento web Flask e a biblioteca de gráficos ApexCharts.</p><br>

###### Requisitos de Software

<li>Python</li>
<li>MongoDB</li>
<li>VSCode</li>

### Instalação

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

### Configurando a base de dados

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

## Nosso Time AJA
You can see more about us in our profile:
* [Amanda](https://github.com/mandis-ncs)
* [Junior](https://github.com/aasjunior)
* [Aline](https://github.com/AlineLauriano)
  
###### Aviso
Esta é uma iniciativa acadêmica, sendo assim, não possui todas as funcionalidades e características de uma aplicação real. Esse projeto não terá continuação, sendo uma decisão do time de finalizar a iniciativa.
