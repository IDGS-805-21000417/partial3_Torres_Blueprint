from wtforms import Form
from flask_wtf import FlaskForm
 
from wtforms import StringField, PasswordField, SelectField, DateField, IntegerField
from wtforms import validators
 
 
class inicioSesion(Form):         
    usuario=StringField('',[validators.DataRequired(message='Campo requerido')])
    password=PasswordField('',[validators.DataRequired(message='Campo requerido')]) 
    
class AlumnosForms(Form):    
    nombre=StringField('',[validators.DataRequired(message='Campo requerido')])
    usuario=StringField('',[validators.DataRequired(message='Campo requerido')])
    password=PasswordField('',[validators.DataRequired(message='Campo requerido')])     
    apellidoP=StringField('',[validators.DataRequired(message='Campo requerido')])
    apellidoM=StringField('',[validators.DataRequired(message='Campo requerido')])
    nacimiento = DateField('', format='%Y-%m-%d', validators=[validators.DataRequired(message='Campo requerido')])  
    grupo=StringField('',[validators.DataRequired(message='Campo requerido')])    
 
class ProfesoresForms(Form):        
    nombre=StringField('',[validators.DataRequired(message='Campo requerido')])
    usuario=StringField('',[validators.DataRequired(message='Campo requerido')])
    password=PasswordField('',[validators.DataRequired(message='Campo requerido')])     
    apellidoP=StringField('',[validators.DataRequired(message='Campo requerido')])
    apellidoM=StringField('',[validators.DataRequired(message='Campo requerido')])
    nacimiento = DateField('', format='%Y-%m-%d', validators=[validators.DataRequired(message='Campo requerido')])  

class Profesores2Forms(Form):    
    id=IntegerField('id',[validators.number_range(min=1, max=20,message='valor no valido')])
    nombre=StringField('',[validators.DataRequired(message='Campo requerido')])
    usuario=StringField('',[validators.DataRequired(message='Campo requerido')])
    password=PasswordField('',[validators.DataRequired(message='Campo requerido')])     
    apellidoP=StringField('',[validators.DataRequired(message='Campo requerido')])
    apellidoM=StringField('',[validators.DataRequired(message='Campo requerido')])
    nacimiento = DateField('', format='%Y-%m-%d', validators=[validators.DataRequired(message='Campo requerido')])  
        
class CuestionarioForms(Form):    
    pregunta=StringField('',[validators.DataRequired(message='Campo requerido')])
    opcion1=StringField('',[validators.DataRequired(message='Campo requerido')])
    opcion2=StringField('',[validators.DataRequired(message='Campo requerido')])
    opcion3=StringField('',[validators.DataRequired(message='Campo requerido')])
    opcion4=StringField('',[validators.DataRequired(message='Campo requerido')])
    correcta=StringField('',[validators.DataRequired(message='Campo requerido')])

class CalificacionesForms(Form):     
    grupo=SelectField('',choices=[],validators=[validators.DataRequired(message='Seleccione un grupo')])  

class ExamenAlumnosForms(Form):         
    nombre=StringField('',[validators.DataRequired(message='Campo requerido')])
    apellidoP=StringField('',[validators.DataRequired(message='Campo requerido')])   
    