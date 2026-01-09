from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
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
    salary_account_number = db.Column(db.String(20), nullable=True)
    salary = db.Column(db.Float, default=0.0) # Salario asignado

    # Images
    selfie_filename = db.Column(db.String(120), nullable=True)
    dni_photo_filename = db.Column(db.String(120), nullable=True)

    # Discord Integration
    discord_id = db.Column(db.String(50), unique=True, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships (Con CASCADE para permitir eliminación limpia de usuarios)
    bank_account = db.relationship('BankAccount', backref='owner', uselist=False, cascade="all, delete-orphan")
    licenses = db.relationship('License', backref='holder', lazy='dynamic', cascade="all, delete-orphan")
    
    # Antecedentes
    criminal_records = db.relationship('CriminalRecord', foreign_keys='CriminalRecord.user_id', backref='subject', lazy='dynamic', cascade="all, delete-orphan")
    authored_reports = db.relationship('CriminalRecord', foreign_keys='CriminalRecord.author_id', backref='author', lazy='dynamic')
    
    traffic_fines = db.relationship('TrafficFine', foreign_keys='TrafficFine.user_id', backref='offender', lazy='dynamic', cascade="all, delete-orphan")
    
    # Comentarios
    comments = db.relationship('Comment', foreign_keys='Comment.user_id', backref='subject_user', lazy='dynamic', cascade="all, delete-orphan")
    
    # Negocios
    businesses = db.relationship('Business', backref='owner', lazy='dynamic', cascade="all, delete-orphan")

    # Lotería
    tickets = db.relationship('LotteryTicket', backref='owner', lazy='dynamic', cascade="all, delete-orphan")

    # Citas (Appointments) - Importante para el error de borrado
    appointments_made = db.relationship('Appointment', foreign_keys='Appointment.citizen_id', backref='citizen', lazy=True, cascade="all, delete-orphan")
    appointments_received = db.relationship('Appointment', foreign_keys='Appointment.official_id', backref='official', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.dni}>'

class BankAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(20), unique=True, index=True)
    balance = db.Column(db.Float, default=0.0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    card_style = db.Column(db.String(20), default='blue') # blue, gold, black, custom
    custom_image = db.Column(db.String(120), nullable=True)
    
    transactions = db.relationship('BankTransaction', backref='account', lazy='dynamic', cascade="all, delete-orphan")
    loans = db.relationship('BankLoan', backref='account', lazy='dynamic', cascade="all, delete-orphan")
    savings = db.relationship('BankSavings', backref='account', lazy='dynamic', cascade="all, delete-orphan")

class BankTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('bank_account.id'))
    type = db.Column(db.String(20))
    amount = db.Column(db.Float)
    related_account = db.Column(db.String(20), nullable=True)
    description = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class BankLoan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('bank_account.id'))
    amount_due = db.Column(db.Float)
    due_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='Active')
    last_penalty_check = db.Column(db.DateTime, nullable=True)

class BankSavings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('bank_account.id'))
    amount = db.Column(db.Float)
    deposit_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Active')

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
    amount = db.Column(db.Float)
    reason = db.Column(db.String(200))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Pendiente')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

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
    
    author = db.relationship('User', foreign_keys=[author_id])

class CriminalRecordSubjectPhoto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120))
    record_id = db.Column(db.Integer, db.ForeignKey('criminal_record.id'))

class CriminalRecordEvidencePhoto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120))
    record_id = db.Column(db.Integer, db.ForeignKey('criminal_record.id'))

class Lottery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    current_jackpot = db.Column(db.Float, default=50000.0)
    last_run_date = db.Column(db.Date)

class LotteryTicket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    numbers = db.Column(db.String(5))
    date = db.Column(db.Date)

class GovernmentFund(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float, default=1000000.0)
    expenses_description = db.Column(db.Text, nullable=True)
    net_benefits = db.Column(db.Float, default=0.0)

class PayrollRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(64))
    total_amount = db.Column(db.Float)
    status = db.Column(db.String(20), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    items = db.relationship('PayrollItem', backref='request', lazy=True, cascade="all, delete-orphan")

class PayrollItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('payroll_request.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    amount = db.Column(db.Float)
    
    user = db.relationship('User')

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    citizen_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    official_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.DateTime)
    reason = db.Column(db.String(200))
    status = db.Column(db.String(20), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow) # AÑADIDO: Campo que faltaba
