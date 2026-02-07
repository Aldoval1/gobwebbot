from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    dni = db.Column(db.String(20), index=True, unique=True)
    password_hash = db.Column(db.String(256))
    
    # Official / Job Info
    badge_id = db.Column(db.String(20), index=True, unique=True, nullable=True)
    department = db.Column(db.String(64), nullable=True)
    official_rank = db.Column(db.String(64), nullable=True)
    official_status = db.Column(db.String(20), default='Pendiente') # Pendiente, Aprobado, Suspendido

    # Images
    selfie_filename = db.Column(db.String(120), nullable=True)
    dni_photo_filename = db.Column(db.String(120), nullable=True)

    # Discord Integration
    discord_id = db.Column(db.String(50), unique=True, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships (Con CASCADE para permitir eliminación limpia de usuarios)
    licenses = db.relationship('License', backref='holder', lazy='dynamic', cascade="all, delete-orphan")
    
    # Antecedentes
    criminal_records = db.relationship('CriminalRecord', foreign_keys='CriminalRecord.user_id', backref='subject', lazy='dynamic', cascade="all, delete-orphan")
    
    # Antecedentes creados POR este usuario (Oficial)
    # backref='author' creates 'record.author' on CriminalRecord automatically.
    authored_reports = db.relationship('CriminalRecord', foreign_keys='CriminalRecord.author_id', backref='author', lazy='dynamic')
    
    traffic_fines = db.relationship('TrafficFine', foreign_keys='TrafficFine.user_id', backref='offender', lazy='dynamic', cascade="all, delete-orphan")
    
    # Comentarios
    comments = db.relationship('Comment', foreign_keys='Comment.user_id', backref='subject_user', lazy='dynamic', cascade="all, delete-orphan")
    
    # Negocios
    businesses = db.relationship('Business', backref='owner', lazy='dynamic', cascade="all, delete-orphan")

    # Citas (Appointments) - Importante para el error de borrado
    appointments_made = db.relationship('Appointment', foreign_keys='Appointment.citizen_id', backref='citizen', lazy=True, cascade="all, delete-orphan")
    appointments_received = db.relationship('Appointment', foreign_keys='Appointment.official_id', backref='official', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.dni}>'

class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    location_x = db.Column(db.Float)
    location_y = db.Column(db.Float)
    photo_filename = db.Column(db.String(120), nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    licenses = db.relationship('License', backref='business', lazy='dynamic', cascade="all, delete-orphan")

class License(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100))
    status = db.Column(db.String(20), default='Activa')
    issue_date = db.Column(db.Date, default=datetime.utcnow().date)
    expiration_date = db.Column(db.Date, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=True)

class TrafficFine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reason = db.Column(db.String(200))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Pendiente')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    author = db.relationship('User', foreign_keys=[author_id])

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    author = db.relationship('User', foreign_keys=[author_id])

class CriminalRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    crime = db.Column(db.String(100))
    penal_code = db.Column(db.String(50))
    report_text = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    subject_photos = db.relationship('CriminalRecordSubjectPhoto', backref='record', lazy=True, cascade="all, delete-orphan")
    evidence_photos = db.relationship('CriminalRecordEvidencePhoto', backref='record', lazy=True, cascade="all, delete-orphan")
    
    # REMOVED EXPLICIT 'author' RELATIONSHIP HERE TO FIX CONFLICT WITH USER BACKREF

class CriminalRecordSubjectPhoto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120))
    record_id = db.Column(db.Integer, db.ForeignKey('criminal_record.id'))

class CriminalRecordEvidencePhoto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120))
    record_id = db.Column(db.Integer, db.ForeignKey('criminal_record.id'))

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    citizen_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    official_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.DateTime)
    reason = db.Column(db.String(200))
    status = db.Column(db.String(20), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow) # AÑADIDO: Campo que faltaba
