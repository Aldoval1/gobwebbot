
from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    db.create_all()
    # Check if admin already exists
    admin = User.query.filter_by(dni='000').first()
    if admin:
        print("Admin user already exists.")
    else:
        # Create a new admin user
        # Note: Adjust fields based on your User model requirements
        # Assuming badge_id='000' is key for super-admin as per context
        admin = User(
            dni='000',
            first_name='Gobierno',
            last_name='Admin',
            badge_id='000',
            department='Gobierno',
            official_status='Aprobado',
            official_rank='Lider',
            on_duty=False,
            # Add other necessary fields with dummy data if needed
            selfie_filename='default.jpg',
            dni_photo_filename='default.jpg'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Admin user (DNI/Badge: 000) created with password 'admin123'.")
