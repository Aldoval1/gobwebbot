from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField, TextAreaField, SelectField, DateField, TimeField, SelectMultipleField, RadioField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Length, NumberRange, Optional
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app.models import User

class LoginForm(FlaskForm):
    dni = StringField('DNI', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Iniciar Sesión')

class RegistrationForm(FlaskForm):
    first_name = StringField('Nombre', validators=[DataRequired()])
    last_name = StringField('Apellido', validators=[DataRequired()])
    dni = StringField('DNI', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('password')])
    selfie = FileField('Selfie', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Solo imágenes')])
    dni_photo = FileField('Foto DNI', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Solo imágenes')])
    submit = SubmitField('Registrarse')

class OfficialLoginForm(FlaskForm):
    badge_id = StringField('Placa ID', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Acceso Funcionario')

class OfficialRegistrationForm(FlaskForm):
    first_name = StringField('Nombre', validators=[DataRequired()])
    last_name = StringField('Apellido', validators=[DataRequired()])
    dni = StringField('DNI', validators=[DataRequired()])
    badge_id = StringField('Placa ID', validators=[DataRequired()])
    department = SelectField('Departamento', choices=[
        ('Policia', 'Policía (LSPD)'), 
        ('Sheriff', 'Sheriff (BCSO)'),
        ('SABES', 'Médicos (SABES)'), 
        ('Mecanico', 'Mecánicos'), 
        ('Taxista', 'Taxistas'),
        ('Gobierno', 'Gobierno')
    ], validators=[DataRequired()])
    account_number = StringField('Cuenta Bancaria Personal', validators=[DataRequired()])
    photo = FileField('Foto Credencial', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Solo imágenes')])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Solicitar Acceso')

class SearchUserForm(FlaskForm):
    query = StringField('Buscar Ciudadano', validators=[DataRequired()])
    submit = SubmitField('Buscar')

class CriminalRecordForm(FlaskForm):
    date = DateField('Fecha del Hecho', format='%Y-%m-%d', validators=[DataRequired()])
    crime = StringField('Delito / Crimen', validators=[DataRequired()])
    penal_code = StringField('Código Penal', validators=[DataRequired()])
    report_text = TextAreaField('Informe Detallado', validators=[DataRequired()])
    subject_photos = SelectMultipleField('Fotos del Sujeto', choices=[], validate_choice=False) # Handled manually
    evidence_photos = SelectMultipleField('Fotos Evidencia', choices=[], validate_choice=False) # Handled manually
    
    # Files upload fields for the form (not model fields)
    subject_photos = FileField('Fotos del Sujeto', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Imágenes only')], render_kw={'multiple': True})
    evidence_photos = FileField('Evidencia', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Imágenes only')], render_kw={'multiple': True})

    submit = SubmitField('Registrar Antecedente')

class TrafficFineForm(FlaskForm):
    amount = FloatField('Monto Multa', validators=[DataRequired()])
    reason = StringField('Razón', validators=[DataRequired()])
    submit = SubmitField('Imponer Multa')

class CommentForm(FlaskForm):
    content = TextAreaField('Comentario', validators=[DataRequired()])
    submit = SubmitField('Agregar Nota')

class TransferForm(FlaskForm):
    account_number = StringField('Cuenta Destino', validators=[DataRequired(), Length(min=10, max=10)])
    amount = FloatField('Monto', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Transferir')

class LoanForm(FlaskForm):
    accept_terms = BooleanField('Acepto los términos', validators=[DataRequired()])
    submit = SubmitField('Solicitar Préstamo Rápido ($5500)')

class LoanRepayForm(FlaskForm):
    amount = FloatField('Monto a Pagar', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Pagar Préstamo')

class SavingsForm(FlaskForm):
    amount = FloatField('Monto a Depositar', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Depositar (Bloqueo 30 días)')

class CardCustomizationForm(FlaskForm):
    style = RadioField('Estilo de Tarjeta', choices=[
        ('blue', 'Azul Clásico'),
        ('gold', 'Gold Elite'),
        ('black', 'Black Infinite'),
        ('custom', 'Personalizado (Subir Imagen)')
    ], default='blue')
    custom_image = FileField('Imagen Personalizada', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Solo imágenes')])
    submit = SubmitField('Guardar Diseño')

class LotteryTicketForm(FlaskForm):
    numbers = StringField('Tus 5 Números', validators=[DataRequired(), Length(min=5, max=5)])
    submit = SubmitField('Comprar Ticket ($500)')

class AdjustBalanceForm(FlaskForm):
    operation = SelectField('Operación', choices=[('add', 'Añadir Fondos (+)'), ('sub', 'Retirar Fondos (-)')])
    amount = FloatField('Cantidad', validators=[DataRequired(), NumberRange(min=0.01)])
    reason = TextAreaField('Motivo del Ajuste', validators=[DataRequired()])
    submit = SubmitField('Aplicar Ajuste')

class GovFundAdjustForm(FlaskForm):
    operation = SelectField('Operación', choices=[('add', 'Ingresar Fondos'), ('sub', 'Retirar Fondos')])
    amount = FloatField('Cantidad', validators=[DataRequired(), NumberRange(min=0.01)])
    submit = SubmitField('Ejecutar')

class SalaryForm(FlaskForm):
    salary = FloatField('Sueldo', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Actualizar Sueldo')

class AppointmentForm(FlaskForm):
    date = DateField('Fecha', validators=[DataRequired()])
    time = TimeField('Hora', validators=[DataRequired()])
    description = TextAreaField('Motivo de la Cita', validators=[DataRequired()])
    submit = SubmitField('Solicitar Cita')

class CreateLeaderForm(FlaskForm):
    first_name = StringField('Nombre', validators=[DataRequired()])
    last_name = StringField('Apellido', validators=[DataRequired()])
    dni = StringField('DNI (Existente)', validators=[DataRequired()])
    badge_id = StringField('Placa ID', validators=[DataRequired()])
    account_number = StringField('Cuenta Bancaria', validators=[DataRequired()])
    department = SelectField('Departamento', choices=[
        ('Policia', 'Policía (LSPD)'), 
        ('Sheriff', 'Sheriff (BCSO)'),
        ('SABES', 'Médicos (SABES)'), 
        ('Mecanico', 'Mecánicos'), 
        ('Taxista', 'Taxistas'),
        ('Gobierno', 'Gobierno')
    ], validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Crear Líder')

class GovFinancialsForm(FlaskForm):
    expenses_description = TextAreaField('Descripción de Gastos y Presupuesto')
    net_benefits = FloatField('Beneficios Netos', validators=[Optional()])
    submit = SubmitField('Actualizar Finanzas')

class EditCitizenForm(FlaskForm):
    first_name = StringField('Nombre', validators=[DataRequired()])
    last_name = StringField('Apellido', validators=[DataRequired()])
    dni = StringField('DNI', validators=[DataRequired()])
    submit = SubmitField('Actualizar Datos')

class EditCitizenPhotoForm(FlaskForm):
    selfie = FileField('Nueva Selfie', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Solo imágenes')])
    dni_photo = FileField('Nueva Foto DNI', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Solo imágenes')])
    submit = SubmitField('Actualizar Fotos')

class BusinessLicenseForm(FlaskForm):
    name = StringField('Nombre del Negocio', validators=[DataRequired()])
    business_type = SelectField('Tipo de Negocio', choices=[
        ('247', 'Tienda 24/7'),
        ('Pharmacy', 'Farmacia'),
        ('Mechanic', 'Taller Mecánico'),
        ('Restaurant', 'Restaurante'),
        ('GasStation', 'Gasolinera'),
        ('Club', 'Discoteca'),
        ('Bar', 'Bar'),
        ('UsedCars', 'Venta Coches Usados'),
        ('SexShop', 'Sex Shop'),
        ('Groceries', 'Verdulería'),
        ('Hardware', 'Ferretería'),
        ('Barber', 'Barbería'),
        ('Clothes', 'Tienda de Ropa')
    ], validators=[DataRequired()])
    location_x = FloatField('Pos X', validators=[DataRequired()])
    location_y = FloatField('Pos Y', validators=[DataRequired()])
    photo = FileField('Foto del Local (Exterior)', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Solo imágenes')])
    submit = SubmitField('Registrar y Pagar')

class UserPhotoForm(FlaskForm):
    photo = FileField('Nueva Foto de Perfil', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Solo imágenes')])
    submit = SubmitField('Actualizar Foto')

# NUEVO: Formulario de Cambio de Contraseña (Admin)
class ChangePasswordForm(FlaskForm):
    new_password = PasswordField('Nueva Contraseña', validators=[DataRequired(), Length(min=3)])
    submit = SubmitField('Establecer Contraseña')
