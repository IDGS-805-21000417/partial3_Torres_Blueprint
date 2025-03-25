from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from models import *
import forms

auth = Blueprint('auth', __name__)


@auth.route("/", methods=['GET', 'POST'])
@auth.route("/index", methods=['GET', 'POST'])
def inicio():
    create_form = forms.inicioSesion(request.form)

    if request.method == 'POST' and create_form.validate():
        usu = create_form.usuario.data.strip()
        pas = create_form.password.data.strip()

        sesion = Alumnos.query.filter_by(usuario=usu, password=pas).first()

        if sesion:
            login_user(sesion)            
            flash("Inicio de sesión.", "success")
            return redirect(url_for('alumnos.examen2'))
        else:
            sesion = Profesores.query.filter_by(usuario=usu, password=pas).first()
            if sesion:
                login_user(sesion)                
                flash("Inicio de sesión.", "success")
                return redirect(url_for('maestros.alumnos'))
            else:                
                flash("Usuario o contraseña incorrectos.", "danger")
                return redirect(url_for('auth.inicio'))

    return render_template("index.html", form=create_form)

@auth.route("/logout")
@login_required
def logout():    
    logout_user()
    flash("Fin de sesión.", "info")
    return redirect(url_for('auth.inicio'))
