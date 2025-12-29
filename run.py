from app import create_app, db
from dotenv import load_dotenv
import os
from flask_migrate import upgrade

# Importar modelos para que SQLAlchemy sepa qué tablas crear
from app.models import (
    User, BankAccount, GovernmentFund, Lottery, 
    TrafficFine, Comment, License, CriminalRecord, 
    LotteryTicket, PayrollRequest, PayrollItem, Appointment
)

load_dotenv()

app = create_app()

# --- BLOQUE DE AUTO-INICIALIZACIÓN ---
# Este código se ejecuta una vez cada vez que Gunicorn arranca la aplicación.
with app.app_context():
    try:
        print("🔄 Verificando estado de la Base de Datos...")
        
        # 0. EJECUTAR MIGRACIONES PENDIENTES
        # Esto soluciona el error 'column does not exist' aplicando los cambios pendientes (alembic)
        print("🛠️ Aplicando migraciones pendientes (Flask-Migrate)...")
        upgrade() 
        print("✅ Migraciones aplicadas.")

        # 1. Crear Tablas (Si no existen)
        # db.create_all() crea las tablas si no existen, pero NO actualiza columnas nuevas.
        # Por eso necesitamos upgrade() arriba.
        db.create_all()
        print("✅ Tablas verificadas.")

        # 2. Inicializar Lotería y Fondo (Si no existen)
        if not GovernmentFund.query.first():
            db.session.add(GovernmentFund(balance=1000000.0))
            print("💰 Fondo de Gobierno inicializado.")
        
        if not Lottery.query.first():
            from datetime import datetime
            db.session.add(Lottery(current_jackpot=50000.0, last_run_date=datetime.utcnow().date()))
            print("🎰 Lotería inicializada.")

        # 3. Crear Super Admin '000' (Si no existe)
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
        print(f"⚠️ Advertencia durante la inicialización: {e}")
        # No detenemos la app, por si es un error menor de conexión temporal

if __name__ == '__main__':
    app.run(debug=True)
