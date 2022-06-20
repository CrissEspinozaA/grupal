import re
from flask_app import app
from flask_app.models.salas import Sala 
from flask_app.models.users import User
from flask_bcrypt import Bcrypt
from flask import render_template, request, redirect, url_for, session, flash 
bcrypt = Bcrypt(app)

@app.route('/crear_sala', methods = [ 'POST']) 
def sala(): 
    if 'user.id_usuario' in session:
        return render_template('crear_sala.html')
    else:
        return redirect('/login')

@app.route('/crear_sala/nueva', methods = ['POST'])
def crear_sala(): 
        data = {
            "nombre_sala": request.form['nombre_sala'],
            "descripcion": request.form['descripcion'],
            "administrador": request.form['administrador'],
            "mayor_edad": request.form['mayor_edad'],
            "id_usuario": session['usuario.id_usuario']
            }
        Sala.crear_sala(data)
        print("guardé bien los datos")
        return redirect('/dashboard')