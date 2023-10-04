# Projeto: VitaLab
Gerenciador de Laboratorio de exames medicos

# Criar o ambiente virtual
    python -m venv venv

# Ativar e desativer o ambiente virtual
    .\venv\Scripts\Activate
    deactivate

# instalar o Django e as demais bibliotecas:
    pip install django

# gerenciador de imagens    
    pip install pillow

# instalar Django Rest Framework (DRF) é um framework de desenvolvimento de APIs para o Django
    pip install djangorestframework

# seu_projeto/settings.py - dever ser configurado setting.py
        INSTALLED_APPS = [
            ...
            'rest_framework',
        ]

# Criar o projeto Django:

    django-admin startproject "nome do Projeto(sem aspas)" . 

# startar o servidor
    python manage.py runserver

# criar arquivos de dependencias dos projetos
    pip freeze > requirements.txt

# instalar as dependencias dos projetos
    pip install -r requirements.txt

# criar as instruções de como nosso modelo deverá ser representado em nossa base de dados
    python manage.py makemigrations

# persistir (criar) as alterações no banco de dados
    python manage.py migrate

# criar novo app
    python manage.py startapp "nome do App"

