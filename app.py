from flask import Flask
from flask_login import LoginManager
from models import *
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig

from blueprints.auth import auth
from blueprints.alumnos import alumnos
from blueprints.maestros import maestros

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.inicio'

@login_manager.user_loader
def load_user(user_id):
    return Alumnos.query.get(int(user_id)) or Profesores.query.get(int(user_id))

app.register_blueprint(auth)
app.register_blueprint(alumnos, url_prefix='/alumnos')
app.register_blueprint(maestros, url_prefix='/maestros')
    
if __name__ == '__main__':
    csrf.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)