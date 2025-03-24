from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from config import DevelopmentConfig
from models import db, Usuarios
import forms

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()
db.init_app(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'inicio' 

@login_manager.user_loader
def load_user(user_id):
    return Usuarios.query.get(int(user_id))

@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def inicio():
    create_form = forms.inicioSesion(request.form)

    if request.method == 'POST' and create_form.validate():
        usu = create_form.usuario.data.strip()
        pas = create_form.password.data.strip()

        sesion = Usuarios.query.filter_by(usuario=usu, password=pas).first()

        if sesion:
            login_user(sesion)
            flash("Inicio de sesion.", "success")
            return redirect(url_for('contenido'))
        else:
            flash("Usuario o contraseña incorrectos.", "danger")
            return redirect(url_for('inicio'))

    return render_template("index.html", form=create_form)

@app.route("/contenido", methods=['GET', 'POST'])
@login_required
def contenido():
    create_form=forms.nuevoUsuario(request.form)
    if request.method=='POST' and create_form.validate():
        
        reg=Usuarios(nombre=create_form.nombre.data,
                     usuario=create_form.usuario.data,
                     password=create_form.password.data)        
        db.session.add(reg)
        db.session.commit()
        flash("Usuario registrado.", "success")
        return redirect(url_for('contenido'))  
      
    return render_template("contenido.html", form=create_form,usuario=current_user.nombre)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Fin de sesion.", "info")
    return redirect(url_for('inicio'))

if __name__ == '__main__':
    csrf.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
