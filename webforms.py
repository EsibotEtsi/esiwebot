from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea

# Formulario de logueo
class LoginForm(FlaskForm):
	username = StringField("Usuario", validators=[DataRequired()])
	password = PasswordField("Contraseña", validators=[DataRequired()])
	submit = SubmitField("Enviar")

#Formulario de Posteo (EN CONSTRUCCIÓN)
class PostForm(FlaskForm):
	title = StringField("Titulo", validators=[DataRequired()])
	content = StringField("Content", validators=[DataRequired()], widget=TextArea())
	
	submit = SubmitField("Enviar")

#Formulario de Usuario
class UserForm(FlaskForm):
	nombre = StringField("Nombre", validators=[DataRequired()])
	usuario = StringField("Usuario", validators=[DataRequired()])
	email = StringField("Email", validators=[DataRequired()])
	password_hash = PasswordField('Contraseña', validators=[DataRequired(), EqualTo('password_hash2', message='¡Las contraseñas deben coincidir!')])
	password_hash2 = PasswordField('Confirmar Contraseña', validators=[DataRequired()])
	submit = SubmitField("Enviar")

#Formulario de Contraseña
class PasswordForm(FlaskForm):
	email = StringField("Cuál es tu email", validators=[DataRequired()])
	password_hash = PasswordField("Cuál es tu contraseña", validators=[DataRequired()])
	submit = SubmitField("Enviar")