# Back-End PratoCerto 🍽️
## 	Inicialização do projeto no _Linux_

### Criação da venv
No terminal: ``virtualenv venv``

### Ativação da venv
No terminal: ``source venv/bin/activate``

### Instalação das dependências necessárias
Após ativação da venv digite no terminal: ``pip install -r requirements.txt``

## Inicialização do projeto no _Windows_
### Criação da venv
No terminal: ``python -m venv venv``

### Ativação da venv
No terminal: ``.\venv\Scripts\activate``

### Instalação das dependências necessárias
Após ativação da venv digite no terminal: ``pip install -r requirements.txt``

## Comandos para inicializar o BD

### Caso não possua no diretorio da aplicação a pasta "migrations"
Digite no terminal com a venv ativa: ``flask db init``

### Para fazer um commit no banco de dados
Digite no terminal: ``flask db migrate -m "mensagem_para_commit"``

### Subindo o commit para o banco de dados
Digite no terminal: ``flask db upgrade``