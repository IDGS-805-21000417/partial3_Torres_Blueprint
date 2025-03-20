from wtforms import Form
from flask_wtf import FlaskForm
 
from wtforms import StringField
from wtforms import validators
 
 
class inicioSesion(Form):         
    usuario=StringField('',[validators.DataRequired(message='Campo requerido')])
    password=StringField('',[validators.DataRequired(message='Campo requerido')]) 