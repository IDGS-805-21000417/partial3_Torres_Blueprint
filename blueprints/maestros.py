from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required 
from models import *
import forms

maestros = Blueprint('maestros', __name__)

@maestros.route("/alumnos", methods=['GET', 'POST'])
@login_required
def alumnos():
    create_form = forms.AlumnosForms(request.form)
    alumno = Alumnos.query.all()
    
    if request.method == 'POST' and create_form.validate():
        alumno = Alumnos(nombre=create_form.nombre.data,
                         usuario=create_form.usuario.data,
                         password=create_form.password.data,
                         apellidoP=create_form.apellidoP.data,
                         apellidoM=create_form.apellidoM.data,
                         nacimiento=create_form.nacimiento.data,
                         grupo=create_form.grupo.data)
        db.session.add(alumno)
        db.session.commit()
        return redirect(url_for('maestros.alumnos'))
    
    return render_template("alumnos.html", form=create_form, alumnos=alumno)

@maestros.route("/profesores", methods=['GET', 'POST'])
@login_required
def profesores():
    create_form = forms.ProfesoresForms(request.form)
    profe = Profesores.query.all()
    
    if request.method == 'POST' and create_form.validate():
        profe = Profesores(nombre=create_form.nombre.data,
                         usuario=create_form.usuario.data,
                         password=create_form.password.data,
                         apellidoP=create_form.apellidoP.data,
                         apellidoM=create_form.apellidoM.data,
                         nacimiento=create_form.nacimiento.data
                         )
        db.session.add(profe)
        db.session.commit()
        return redirect(url_for('maestros.profesores'))
    
    return render_template("profesores.html", form=create_form, profesores=profe)

@maestros.route("/eliminar/<int:id>", methods=['POST'])
@login_required
def eliminar(id):
    
    profe = Profesores.query.get_or_404(id)
    
    db.session.delete(profe)
    db.session.commit()
    
    return redirect(url_for('maestros.profesores'))

@maestros.route("/modificar", methods=['GET', 'POST'])
@login_required
def modificar():
    create_form=forms.Profesores2Forms(request.form)
    if request.method=='GET':
        id=request.args.get('id')        
        profe=db.session.query(Profesores).filter(Profesores.id==id).first()
        create_form.id.data=request.args.get('id')
        create_form.nombre.data=str.rstrip(profe.nombre)
        create_form.usuario.data=profe.usuario
        create_form.apellidoP.data=profe.apellidoP
        create_form.apellidoM.data=profe.apellidoM
        create_form.nacimiento.data=profe.nacimiento
        
    if request.method=='POST':
        id=create_form.id.data
        profe=db.session.query(Profesores).filter(Profesores.id==id).first()
        profe.id=id
        profe.nombre=str.rstrip(create_form.nombre.data)
        profe.usuario=create_form.usuario.data
        profe.apellidoP=create_form.apellidoP.data
        profe.apellidoM=create_form.apellidoM.data
        profe.nacimiento=create_form.nacimiento.data    
        
        db.session.add(profe)
        db.session.commit()
        return redirect(url_for('maestros.profesores'))
    return render_template('modificar.html',form=create_form)

@maestros.route("/preguntas", methods=['GET', 'POST'])
@login_required
def preguntas():
    create_form = forms.CuestionarioForms(request.form)
    pregunta = Cuestionario.query.all()
    
    if request.method == 'POST' and create_form.validate():
        pregunta = Cuestionario(pregunta=create_form.pregunta.data,
                                opcion1=create_form.opcion1.data,
                                opcion2=create_form.opcion2.data,
                                opcion3=create_form.opcion3.data,
                                opcion4=create_form.opcion4.data,
                                correcta=create_form.correcta.data)
        db.session.add(pregunta)
        db.session.commit()
        return redirect(url_for('maestros.preguntas'))
    
    return render_template("preguntas.html", form=create_form, preguntas=pregunta)

@maestros.route("/calificaciones", methods=['GET', 'POST'])
@login_required
def calificaciones():
    create_form = forms.CalificacionesForms(request.form)
    grupos = db.session.query(Alumnos.grupo).distinct().all()
    create_form.grupo.choices = [(g.grupo, g.grupo) for g in grupos]
    
    alumno = []
    
    if request.method == 'POST':
        grupo = create_form.grupo.data
        alumno = db.session.query(Alumnos).filter(Alumnos.grupo == grupo).all()

    return render_template("calificaciones.html", form=create_form, alumnos=alumno)

@maestros.route("/examen", methods=['GET', 'POST'])
@login_required
def examen():
    create_form = forms.ExamenAlumnosForms(request.form)
    preguntas = Cuestionario.query.all()
    accion = request.form.get('accion')
    alumno = None
    edad = 0
    calificacion = 0    
    
    if request.method == 'POST' and create_form.validate() and accion == 'of':        
        nombre = create_form.nombre.data.strip()
        apellidoP = create_form.apellidoP.data.strip()
                
        alumno = db.session.query(Alumnos).filter(Alumnos.nombre == nombre, Alumnos.apellidoP == apellidoP).first()
        
        if alumno:
            edad = 2025 - alumno.nacimiento.year                      

            return render_template("examen.html", form=create_form, alumno=alumno, preguntas=preguntas, edad=edad, nombre=alumno.nombre, apellidoP=alumno.apellidoP)
        else:
            flash("Alumno no encontrado")
            return redirect(url_for('maestros.examen'))

    if request.method == 'POST' and accion == 'on':   
        nombreGlo = request.form.get('nombre', None)
        apelGlo = request.form.get('apellidoP', None)         
        
        alumno = db.session.query(Alumnos).filter(Alumnos.nombre == nombreGlo, Alumnos.apellidoP == apelGlo).first()
        
        if alumno:
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
            return redirect(url_for('maestros.calificaciones'))
        else:
            flash("Alumno no encontrado")
            return redirect(url_for('maestros.examen'))    
    return render_template("examen.html", form=create_form, alumno=alumno, preguntas=preguntas, edad=edad)
