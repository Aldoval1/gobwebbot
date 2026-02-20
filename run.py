from app import create_app, db
from dotenv import load_dotenv
import os
from flask_migrate import upgrade
from sqlalchemy import text, inspect
from sqlalchemy.exc import ProgrammingError, InvalidRequestError

# Importar modelos para que SQLAlchemy sepa qué tablas crear
from app.models import (
    User, TrafficFine, Comment, License, CriminalRecord,
    Appointment, Business, Document
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

        # 3. Defensive Migration: Check for missing columns (Postgres/SQLite compatible)
        try:
            inspector = inspect(db.engine)
            user_columns = [col['name'] for col in inspector.get_columns('user')]

            # Check for 'on_duty'
            if 'on_duty' not in user_columns:
                print("⚠️ Columna 'on_duty' faltante en tabla 'user'. Agregando...")
                with db.engine.connect() as conn:
                    # Generic SQL that works for both if the default is handled carefully
                    # Postgres: BOOLEAN DEFAULT FALSE
                    # SQLite: BOOLEAN DEFAULT 0 (False)
                    # We use SQLAlchemy text() for raw execution.
                    # Note: SQLite doesn't support 'FALSE' keyword in some versions, but 0 works for both as boolean.
                    # However, Postgres implies TRUE/FALSE.
                    # Let's check dialect.
                    if db.engine.dialect.name == 'postgresql':
                        conn.execute(text('ALTER TABLE "user" ADD COLUMN on_duty BOOLEAN DEFAULT FALSE'))
                    else:
                        conn.execute(text('ALTER TABLE "user" ADD COLUMN on_duty BOOLEAN DEFAULT 0'))
                    conn.commit()
                print("✅ Columna 'on_duty' agregada.")

            # Check for 'receive_notifications'
            if 'receive_notifications' not in user_columns:
                print("⚠️ Columna 'receive_notifications' faltante en tabla 'user'. Agregando...")
                with db.engine.connect() as conn:
                    if db.engine.dialect.name == 'postgresql':
                        conn.execute(text('ALTER TABLE "user" ADD COLUMN receive_notifications BOOLEAN DEFAULT TRUE'))
                    else:
                        conn.execute(text('ALTER TABLE "user" ADD COLUMN receive_notifications BOOLEAN DEFAULT 1'))
                    conn.commit()
                print("✅ Columna 'receive_notifications' agregada.")

            # Check for 'created_at' in Appointment (mentioned in comments)
            appointment_columns = [col['name'] for col in inspector.get_columns('appointment')]
            if 'created_at' not in appointment_columns:
                print("⚠️ Columna 'created_at' faltante en tabla 'appointment'. Agregando...")
                with db.engine.connect() as conn:
                    # TIMESTAMP for Postgres, DATETIME for SQLite.
                    # Using generic SQL might be tricky.
                    # Postgres: TIMESTAMP DEFAULT NOW()
                    # SQLite: DATETIME DEFAULT CURRENT_TIMESTAMP
                    if db.engine.dialect.name == 'postgresql':
                         conn.execute(text('ALTER TABLE appointment ADD COLUMN created_at TIMESTAMP DEFAULT NOW()'))
                    else:
                         conn.execute(text('ALTER TABLE appointment ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP'))
                    conn.commit()
                print("✅ Columna 'created_at' agregada a Appointment.")

        except Exception as e:
            print(f"❌ Error en Defensive Migration: {e}")


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
