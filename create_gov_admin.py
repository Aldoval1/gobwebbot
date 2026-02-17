from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

def create_government_admin():
    with app.app_context():
        # 1. Configuración del Admin
        BADGE_ID = "000"
        PASSWORD = "000"
        DNI = "00000000A"  # DNI ficticio para el admin
        DEPT = "Gobierno"
        RANK = "Lider"
        
        print(f"--- Creando/Actualizando Admin de {DEPT} ---")

        # 2. Verificar si ya existe por Placa
        admin_user = User.query.filter_by(badge_id=BADGE_ID).first()
        
        if admin_user:
            print(f"⚠️ El usuario con Placa {BADGE_ID} ya existe.")
            # Actualizamos contraseña y rango por si acaso
            admin_user.set_password(PASSWORD)
            admin_user.official_rank = RANK
            admin_user.official_status = 'Aprobado'
            admin_user.department = DEPT
            print("✅ Datos actualizados (Pass: 000, Rango: Lider).")
        else:
            # 3. Crear nuevo usuario
            # Necesitamos un DNI único. Si el DNI 000... ya existe, lo usamos.
            citizen = User.query.filter_by(dni=DNI).first()
            if not citizen:
                print("Creando perfil de ciudadano base...")
                citizen = User(
                    first_name="Admin",
                    last_name="Sistema",
                    dni=DNI,
                    selfie_filename="default.jpg",
                    dni_photo_filename="default.jpg"
                )
                citizen.set_password(PASSWORD)
                db.session.add(citizen)
                db.session.commit()
                
            print("Creando perfil de funcionario...")
            admin_user = User(
                first_name="Admin",
                last_name="Gobierno",
                dni=citizen.dni, # Vinculado al DNI ciudadano
                badge_id=BADGE_ID,
                department=DEPT,
                official_rank=RANK,
                official_status='Aprobado',
                selfie_filename="default.jpg"
            )
            admin_user.set_password(PASSWORD)
            db.session.add(admin_user)
            print(f"✅ Usuario Admin creado exitosamente.")

        db.session.commit()
        print("------------------------------------------------")
        print(f"Login Oficial: http://127.0.0.1:5000/official/login")
        print(f"Placa: {BADGE_ID}")
        print(f"Pass : {PASSWORD}")

if __name__ == "__main__":
    create_government_admin()