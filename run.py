from app import create_app, db
from dotenv import load_dotenv
import os
from flask_migrate import upgrade
from sqlalchemy import text, inspect
from sqlalchemy.exc import ProgrammingError, InvalidRequestError

# Importar modelos para que SQLAlchemy sepa qué tablas crear
from app.models import (
    User, TrafficFine, Comment, License, CriminalRecord,
    Appointment, Business
)

load_dotenv()

app = create_app()

# --- BLOQUE DE AUTO-INICIALIZACIÓN ---
# Este código se ejecuta una vez cada vez que Gunicorn arranca la aplicación.
with app.app_context():
    try:
        print("🔄 Verificando estado de la Base de Datos...")
        
        # 2. Crear Tablas (Si no existen, incluyendo Business)
        try:
            db.create_all()
            print("✅ Tablas verificadas.")
        except Exception as e:
             print(f"❌ Error genérico en create_all: {e}")

        # 4. Crear Super Admin '000' (Si no existe)
        admin = User.query.filter_by(badge_id="000").first()
        if not admin:
            print("🚀 Creando Usuario Admin (000/000)...")
            
            # Crear ciudadano base para el admin
            admin = User(
                first_name="Admin",
                last_name="Gobierno",
                dni="00000000A",
                badge_id="000",
                department="Gobierno",
                official_rank="Lider",
                official_status="Aprobado",
                selfie_filename="default.jpg",
                dni_photo_filename="default.jpg"
            )
            admin.set_password("000")
            db.session.add(admin)
            
            print("✅ Usuario Admin creado exitosamente.")

        db.session.commit()
        print("✨ Inicialización completada.")

    except Exception as e:
        print(f"⚠️ Advertencia crítica durante la inicialización: {e}")
        # No detenemos la app

if __name__ == '__main__':
    app.run(debug=True)
