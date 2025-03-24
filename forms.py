from wtforms import Form
from flask_wtf import FlaskForm
 
from wtforms import StringField, PasswordField
from wtforms import validators
 
 
class inicioSesion(Form):         
    usuario=StringField('',[validators.DataRequired(message='Campo requerido')])
    password=PasswordField('',[validators.DataRequired(message='Campo requerido')]) 
    
class nuevoUsuario(Form):         
    nombre=StringField('',[validators.DataRequired(message='Campo requerido')])
    usuario=StringField('',[validators.DataRequired(message='Campo requerido')])
    password=PasswordField('',[validators.DataRequired(message='Campo requerido')])     