from app import create_app, db
from dotenv import load_dotenv
import os
from flask_migrate import upgrade
from sqlalchemy import text, inspect
from sqlalchemy.exc import ProgrammingError

# Importar modelos para que SQLAlchemy sepa qué tablas crear
from app.models import (
    User, BankAccount, GovernmentFund, Lottery, 
    TrafficFine, Comment, License, CriminalRecord, 
    LotteryTicket, PayrollRequest, PayrollItem, Appointment, Business
)

load_dotenv()

app = create_app()

# --- BLOQUE DE AUTO-INICIALIZACIÓN ---
# Este código se ejecuta una vez cada vez que Gunicorn arranca la aplicación.
with app.app_context():
    try:
        print("🔄 Verificando estado de la Base de Datos...")
        
        # 0. INTENTO DE MIGRACIÓN (Flask-Migrate)
        try:
            print("🛠️ Aplicando migraciones pendientes...")
            upgrade() 
            print("✅ Migraciones aplicadas.")
        except Exception as e:
            # Es normal que falle si la DB ya está al día o hay conflictos menores
            print(f"⚠️ Nota sobre upgrade(): {e}")

        # 1. REPARACIÓN MANUAL DE SCHEMA (Si las migraciones fallan)
        try:
            inspector = inspect(db.engine)
            
            # --- REPARACIÓN FONDO GOBIERNO ---
            if 'government_fund' in inspector.get_table_names():
                existing_columns = [col['name'] for col in inspector.get_columns('government_fund')]
                if 'expenses_description' not in existing_columns:
                    print("🔧 Reparando DB: Agregando columna 'expenses_description'...")
                    with db.engine.connect() as conn:
                        conn.execute(text("ALTER TABLE government_fund ADD COLUMN expenses_description TEXT"))
                        conn.commit()
                if 'net_benefits' not in existing_columns:
                    print("🔧 Reparando DB: Agregando columna 'net_benefits'...")
                    with db.engine.connect() as conn:
                        conn.execute(text("ALTER TABLE government_fund ADD COLUMN net_benefits FLOAT DEFAULT 0.0"))
                        conn.commit()
            
            # --- REPARACIÓN LICENCIAS (Nuevo Business ID) ---
            if 'license' in inspector.get_table_names():
                existing_columns = [col['name'] for col in inspector.get_columns('license')]
                if 'business_id' not in existing_columns:
                    print("🔧 Reparando DB: Agregando columna 'business_id' a License...")
                    with db.engine.connect() as conn:
                        conn.execute(text("ALTER TABLE license ADD COLUMN business_id INTEGER REFERENCES business(id)"))
                        conn.commit()

        except Exception as e:
            print(f"⚠️ Error en inspección manual: {e}")

        # 2. Crear Tablas (Si no existen, incluyendo Business)
        try:
            # db.create_all() intenta crear tablas. Si ya existen y falla, capturamos el error.
            db.create_all()
            print("✅ Tablas verificadas.")
        except ProgrammingError as e:
            if "already exists" in str(e):
                print("⚠️ Tablas ya existen (Error ignorado, continuando).")
            else:
                print(f"❌ Error en create_all: {e}")
        except Exception as e:
             print(f"❌ Error genérico en create_all: {e}")

        # 3. Inicializar Lotería y Fondo (Si no existen)
        if not GovernmentFund.query.first():
            # INICIALIZACIÓN EN 0.0 (PETICIÓN DE USUARIO)
            db.session.add(GovernmentFund(balance=0.0))
            print("💰 Fondo de Gobierno inicializado en 0.00.")
        
        if not Lottery.query.first():
            from datetime import datetime
            db.session.add(Lottery(current_jackpot=50000.0, last_run_date=datetime.utcnow().date()))
            print("🎰 Lotería inicializada.")

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
                dni_photo_filename="default.jpg",
                salary_account_number="GOV-000"
            )
            admin.set_password("000")
            db.session.add(admin)
            
            # Crear cuenta bancaria asociada al gobierno
            admin_bank = BankAccount(
                account_number="GOV-000",
                balance=10000000.0,
                owner=admin
            )
            db.session.add(admin_bank)
            
            print("✅ Usuario Admin creado exitosamente.")

        db.session.commit()
        print("✨ Inicialización completada.")

    except Exception as e:
        print(f"⚠️ Advertencia crítica durante la inicialización: {e}")
        # No detenemos la app

if __name__ == '__main__':
    app.run(debug=True)
