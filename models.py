from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()
   
class Alumnos(db.Model, UserMixin):
    __tablename__='alumnos'
    id=db.Column(db.Integer,primary_key=True)
    nombre=db.Column(db.String(50))
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    apellidoP=db.Column(db.String(50))
    apellidoM=db.Column(db.String(50))
    nacimiento=db.Column(db.Date)
    grupo=db.Column(db.String(50))
    calificacion = db.Column(db.Float, default=0) 
    
    def get_id(self):
        return str(self.id)

class Profesores(db.Model, UserMixin):
    __tablename__='profesores'
    id=db.Column(db.Integer,primary_key=True)
    nombre=db.Column(db.String(50))
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    apellidoP=db.Column(db.String(50))
    apellidoM=db.Column(db.String(50))
    nacimiento=db.Column(db.Date)
    
    def get_id(self):
        return str(self.id)    
    
class Cuestionario(db.Model, UserMixin):
    __tablename__='cuestionario'
    id=db.Column(db.Integer,primary_key=True)
    pregunta=db.Column(db.String(255))
    opcion1=db.Column(db.String(255))
    opcion2=db.Column(db.String(255))
    opcion3=db.Column(db.String(255))
    opcion4=db.Column(db.String(255))
    correcta=db.Column(db.String(255))    

