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
        ('Ejecutivo', 'Funcionario (Ejecutivo)'),
        ('Legislativo', 'Congresista (Legislativo)'),
        ('Judicial', 'Juez (Judicial)'),
        ('SABES', 'Agente (SABES)')
    ], validators=[DataRequired()])
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
    subject_photos = FileField('Fotos del Sujeto', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Imágenes only')], render_kw={'multiple': True})
    evidence_photos = FileField('Evidencia', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Imágenes only')], render_kw={'multiple': True})

    submit = SubmitField('Registrar Antecedente')

class TrafficFineForm(FlaskForm):
    reason = StringField('Razón', validators=[DataRequired()])
    submit = SubmitField('Imponer Multa')

class CommentForm(FlaskForm):
    content = TextAreaField('Comentario', validators=[DataRequired()])
    submit = SubmitField('Agregar Nota')

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
    department = SelectField('Departamento', choices=[
        ('Ejecutivo', 'Funcionario (Ejecutivo)'),
        ('Legislativo', 'Congresista (Legislativo)'),
        ('Judicial', 'Juez (Judicial)'),
        ('SABES', 'Agente (SABES)'),
        ('Gobierno', 'Gobierno')
    ], validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Crear Líder')

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
    submit = SubmitField('Registrar')

class UserPhotoForm(FlaskForm):
    photo = FileField('Nueva Foto de Perfil', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Solo imágenes')])
    submit = SubmitField('Actualizar Foto')

# NUEVO: Formulario de Cambio de Contraseña (Admin)
class ChangePasswordForm(FlaskForm):
    new_password = PasswordField('Nueva Contraseña', validators=[DataRequired(), Length(min=3)])
    submit = SubmitField('Establecer Contraseña')
