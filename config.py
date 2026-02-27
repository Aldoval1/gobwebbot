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

    # Discord Guilds & Roles
    DISCORD_BOT_TOKEN = os.environ.get('DISCORD_TOKEN')

    GOBIERNO_GUILD_ID = os.environ.get('GOBIERNO_GUILD_ID') or '1407095652718215480'
    JUDICIAL_GUILD_ID = os.environ.get('JUDICIAL_GUILD_ID') or '1451589869397737625'
    CONGRESO_GUILD_ID = os.environ.get('CONGRESO_GUILD_ID') or '1461529761783353347'

    JUDICIAL_ROLE_ID = os.environ.get('JUDICIAL_ROLE_ID') or '1473865577993994260'
    CONGRESO_ROLE_ID = os.environ.get('CONGRESO_ROLE_ID') or '1473835075375337740'
