from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, FloatField, DateField, MultipleFileField, TimeField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, EqualTo, NumberRange, Length, Regexp

class LoginForm(FlaskForm):
    dni = StringField('DNI', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recordar datos')
    submit = SubmitField('Iniciar Sesión')

class RegistrationForm(FlaskForm):
    first_name = StringField('Nombre', validators=[DataRequired()])
    last_name = StringField('Apellido', validators=[DataRequired()])
    dni = StringField('DNI', validators=[DataRequired()])
    selfie = FileField('Foto Selfie', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Solo imágenes permitidas')
    ])
    dni_photo = FileField('Foto DNI', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Solo imágenes permitidas')
    ])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[
        DataRequired(),
        EqualTo('password', message='Las contraseñas deben coincidir')
    ])
    submit = SubmitField('Registrarse')

class OfficialLoginForm(FlaskForm):
    badge_id = StringField('Placa de ID', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recordar datos')
    submit = SubmitField('Entrar')

class OfficialRegistrationForm(FlaskForm):
    first_name = StringField('Nombre', validators=[DataRequired()])
    last_name = StringField('Apellido', validators=[DataRequired()])
    dni = StringField('DNI', validators=[DataRequired()])
    badge_id = StringField('Placa de ID', validators=[DataRequired()])
    account_number = StringField('Número de Cuenta Bancaria', validators=[DataRequired()])
    department = SelectField('Departamento', choices=[
        ('Gobierno', 'Gobierno'),
        ('Policia', 'Policia'),
        ('SABES', 'SABES'),
        ('Sheriff', 'Sheriff'),
        ('LSFD', 'LSFD'),
        ('Universidad', 'Universidad')
    ], validators=[DataRequired()])
    photo = FileField('Foto Personal', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Solo imágenes permitidas')
    ])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[
        DataRequired(),
        EqualTo('password', message='Las contraseñas deben coincidir')
    ])
    submit = SubmitField('Solicitar Registro')

class CreateLeaderForm(FlaskForm):
    first_name = StringField('Nombre', validators=[DataRequired()])
    last_name = StringField('Apellido', validators=[DataRequired()])
    dni = StringField('DNI', validators=[DataRequired()])
    badge_id = StringField('Placa de ID', validators=[DataRequired()])
    account_number = StringField('Cuenta Bancaria', validators=[DataRequired()])
    department = SelectField('Departamento', choices=[
        ('Gobierno', 'Gobierno'),
        ('Policia', 'Policia'),
        ('SABES', 'SABES'),
        ('Sheriff', 'Sheriff'),
        ('LSFD', 'LSFD'),
        ('Universidad', 'Universidad')
    ], validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Crear Líder')

class SearchUserForm(FlaskForm):
    query = StringField('Buscar por Nombre o DNI', validators=[DataRequired()])
    submit = SubmitField('Buscar')

class CriminalRecordForm(FlaskForm):
    date = DateField('Fecha del Suceso', format='%Y-%m-%d', validators=[DataRequired()])
    crime = StringField('Delito Cometido', validators=[DataRequired()])
    penal_code = StringField('Código Penal Infringido', validators=[DataRequired()])
    report_text = TextAreaField('Informe Detallado', validators=[DataRequired()])
    subject_photos = MultipleFileField('Fotos del Sujeto', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Solo imágenes permitidas')
    ])
    evidence_photos = MultipleFileField('Evidencia Fotográfica', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Solo imágenes permitidas')
    ])
    submit = SubmitField('Agregar Antecedente')

class TrafficFineForm(FlaskForm):
    amount = FloatField('Monto de la Multa', validators=[DataRequired()])
    reason = StringField('Motivo', validators=[DataRequired()])
    submit = SubmitField('Imponer Multa')

class CommentForm(FlaskForm):
    content = TextAreaField('Comentario', validators=[DataRequired()])
    submit = SubmitField('Agregar Comentario')

class LicenseForm(FlaskForm):
    type = SelectField('Tipo de Licencia', choices=[
        ('Conducir', 'Conducir'),
        ('Armas', 'Armas'),
        ('Caza', 'Caza'),
        ('Pesca', 'Pesca'),
        ('Negocio', 'Negocio')
    ], validators=[DataRequired()])
    expiration_date = DateField('Fecha de Vencimiento', format='%Y-%m-%d')
    submit = SubmitField('Asignar Licencia')

# Banking Forms
class TransferForm(FlaskForm):
    account_number = StringField('Número de Cuenta', validators=[DataRequired()])
    amount = FloatField('Cantidad', validators=[DataRequired(), NumberRange(min=0.01)])
    submit = SubmitField('Transferir')

class LoanForm(FlaskForm):
    accept_terms = BooleanField('Acepto las condiciones: Pagaré $6000 en 14 días.', validators=[DataRequired()])
    submit = SubmitField('Solicitar Préstamo')

class LoanRepayForm(FlaskForm):
    amount = FloatField('Cantidad a Pagar', validators=[DataRequired(), NumberRange(min=0.01)])
    submit = SubmitField('Pagar')

class SavingsForm(FlaskForm):
    amount = FloatField('Cantidad a Depositar', validators=[DataRequired(), NumberRange(min=0.01)])
    submit = SubmitField('Depositar')

class CardCustomizationForm(FlaskForm):
    style = SelectField('Estilo', choices=[('blue', 'Azul Clásico'), ('gold', 'Oro Premium'), ('black', 'Negro Elite'), ('custom', 'Personalizado')])
    custom_image = FileField('Imagen Personalizada', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Solo imágenes!')])
    submit = SubmitField('Guardar Diseño')

# Lottery Form
class LotteryTicketForm(FlaskForm):
    numbers = StringField('Tus 5 Números', validators=[
        DataRequired(),
        Length(min=5, max=5, message='Deben ser exactamente 5 dígitos'),
        Regexp('^[0-9]*$', message='Solo se permiten números')
    ])
    submit = SubmitField('Comprar Ticket ($500)')

# Government Forms
class AdjustBalanceForm(FlaskForm):
    amount = FloatField('Cantidad', validators=[DataRequired(), NumberRange(min=0.01)])
    operation = SelectField('Operación', choices=[('add', 'Añadir Dinero'), ('subtract', 'Quitar Dinero')], validators=[DataRequired()])
    reason = StringField('Motivo', validators=[DataRequired()])
    submit = SubmitField('Aplicar Ajuste')

class GovFundAdjustForm(FlaskForm):
    amount = FloatField('Cantidad', validators=[DataRequired(), NumberRange(min=0.01)])
    operation = SelectField('Operación', choices=[('add', 'Ingresar Fondos'), ('subtract', 'Retirar Fondos')], validators=[DataRequired()])
    reason = StringField('Motivo', validators=[DataRequired()])
    submit = SubmitField('Ajustar Fondo')

class SalaryForm(FlaskForm):
    salary = FloatField('Salario', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Guardar')

class AppointmentForm(FlaskForm):
    date = DateField('Fecha', format='%Y-%m-%d', validators=[DataRequired()])
    time = TimeField('Hora', format='%H:%M', validators=[DataRequired()])
    description = TextAreaField('Motivo de la Cita', validators=[DataRequired()])
    submit = SubmitField('Solicitar Cita')
