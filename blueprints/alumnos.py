from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import *
import forms

alumnos = Blueprint('alumnos', __name__)

@alumnos.route("/calificaciones2", methods=['GET', 'POST'])
@login_required
def calificaciones2():
    create_form = forms.CalificacionesForms(request.form)
    grupos = db.session.query(Alumnos.grupo).distinct().all()
    create_form.grupo.choices = [(g.grupo, g.grupo) for g in grupos]
    
    alumno = current_user
    alumno_grupo = alumno.grupo if alumno else None

    if request.method == 'POST' and create_form.grupo.data:
        grupo = create_form.grupo.data
        alumnos = db.session.query(Alumnos).filter(Alumnos.grupo == grupo).all()
    else:
        alumnos = db.session.query(Alumnos).filter(Alumnos.grupo == alumno_grupo).all()

    return render_template("calificaciones2.html", form=create_form, alumnos=alumnos)

@alumnos.route("/examen2", methods=['GET', 'POST'])
@login_required
def examen2():
    create_form = forms.ExamenAlumnosForms(request.form)
    preguntas = Cuestionario.query.all()
    accion = request.form.get('accion')
    alumno = current_user  
    edad = 0
    calificacion = 0    
    
    if request.method == 'POST' and create_form.validate() and accion == 'of':        
    
        if alumno:
            edad = 2025 - alumno.nacimiento.year                      

            return render_template("examen2.html", form=create_form, alumno=alumno, preguntas=preguntas, edad=edad, nombre=alumno.nombre, apellidoP=alumno.apellidoP)
        else:
            flash("Alumno no encontrado")
            return redirect(url_for('alumnos.examen2'))

    if request.method == 'POST' and accion == 'on':   
    
        correctas = 0
        totalPreguntas = len(preguntas)

        for pregunta in preguntas:
            respuesta = request.form.get(str(pregunta.id))
            pre = db.session.query(Cuestionario).filter(Cuestionario.id == pregunta.id).first()

            if respuesta == pre.correcta:
                correctas += 1
        
        if totalPreguntas > 0:
            calificacion = (correctas / totalPreguntas) * 10
            
            alumno.calificacion = calificacion
            db.session.commit()

            flash("Calificación registrada.")
        return redirect(url_for('alumnos.calificaciones2'))
    
    return render_template("examen2.html", form=create_form, alumno=alumno, preguntas=preguntas, edad=edad)
