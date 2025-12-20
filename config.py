import os
from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'una-clave-secreta-muy-segura-dev'
    
    # Configuración de rutas
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'img')
    
    # BASE DE DATOS
    # Prioridad: 1. Variable de entorno (Railway/Postgres local) 2. SQLite local
    # IMPORTANTE: Para Postgres se requiere el driver postgresql:// (algunas veces Railway da postgres:// y hay que corregirlo)
    uri = os.environ.get('DATABASE_URL')
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    
    SQLALCHEMY_DATABASE_URI = uri or 'sqlite:///' + os.path.join(basedir, 'hermes_local.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración del Bot (URL interna para comunicación)
    # En local suele ser http://127.0.0.1:8080
    BOT_URL = os.environ.get('BOT_URL') or 'http://127.0.0.1:8080'