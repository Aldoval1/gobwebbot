from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    dni = db.Column(db.String(20), index=True)
    selfie_filename = db.Column(db.String(128))
    dni_photo_filename = db.Column(db.String(128))
    
    # CORRECCIÓN: Aumentado de 128 a 256 para soportar nuevos hash scrypt
    password_hash = db.Column(db.String(256))
    
    # Campo para Discord
    discord_id = db.Column(db.String(32), nullable=True)

    # Official fields
    badge_id = db.Column(db.String(20), index=True, unique=True, nullable=True)
    department = db.Column(db.String(50), nullable=True)
    official_rank = db.Column(db.String(20), default='Miembro')
    official_status = db.Column(db.String(20), default=None)

    # Salary
    salary = db.Column(db.Float, default=0.0)
    salary_account_number = db.Column(db.String(20), nullable=True)

    # Meta
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    comments = db.relationship('Comment', foreign_keys='Comment.user_id', backref='citizen', lazy=True)
    traffic_fines = db.relationship('TrafficFine', foreign_keys='TrafficFine.user_id', backref='citizen', lazy=True)
    licenses = db.relationship('License', backref='citizen', lazy=True)
    criminal_records = db.relationship('CriminalRecord', foreign_keys='CriminalRecord.user_id', backref='citizen', lazy=True)
    bank_account = db.relationship('BankAccount', backref='owner', uselist=False)
    lottery_tickets = db.relationship('LotteryTicket', backref='owner', lazy=True)
    appointments = db.relationship('Appointment', foreign_keys='Appointment.citizen_id', backref='citizen', lazy=True)
    appointments_received = db.relationship('Appointment', foreign_keys='Appointment.official_id', backref='official', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', foreign_keys=[author_id])

class TrafficFine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    reason = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Pendiente')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', foreign_keys=[author_id])

class License(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='Activa')
    expiration_date = db.Column(db.Date, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class CriminalRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    crime = db.Column(db.String(100), nullable=False)
    penal_code = db.Column(db.String(50))
    report_text = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', foreign_keys=[author_id])
    subject_photos = db.relationship('CriminalRecordSubjectPhoto', backref='record', lazy=True, cascade="all, delete-orphan")
    evidence_photos = db.relationship('CriminalRecordEvidencePhoto', backref='record', lazy=True, cascade="all, delete-orphan")

class CriminalRecordSubjectPhoto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(128), nullable=False)
    record_id = db.Column(db.Integer, db.ForeignKey('criminal_record.id'), nullable=False)

class CriminalRecordEvidencePhoto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(128), nullable=False)
    record_id = db.Column(db.Integer, db.ForeignKey('criminal_record.id'), nullable=False)

class BankAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(20), unique=True, nullable=False)
    balance = db.Column(db.Float, default=0.0)
    card_style = db.Column(db.String(20), default='blue')
    custom_image = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    loans = db.relationship('BankLoan', backref='account', lazy=True)
    savings = db.relationship('BankSavings', backref='account', lazy=True)
    transactions = db.relationship('BankTransaction', foreign_keys='BankTransaction.account_id', backref='account', lazy=True)

class BankTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('bank_account.id'), nullable=False)
    type = db.Column(db.String(20))
    amount = db.Column(db.Float, nullable=False)
    related_account = db.Column(db.String(20))
    description = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class BankLoan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('bank_account.id'), nullable=False)
    amount_due = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=False)
    last_penalty_check = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='Active')

class BankSavings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('bank_account.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    deposit_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Active')

class Lottery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    current_jackpot = db.Column(db.Float, default=50000.0)
    last_run_date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)

class LotteryTicket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    numbers = db.Column(db.String(5), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)

class GovernmentFund(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float, default=1000000.0)

class PayrollRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(50), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship('PayrollItem', backref='request', lazy=True, cascade="all, delete-orphan")

class PayrollItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('payroll_request.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    user = db.relationship('User')

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    citizen_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    official_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), default='Pending')