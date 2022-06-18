import bcrypt
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models.modelo_login import Usuario

from flask import render_template, redirect, session, request, flash
bcrypt = Bcrypt(app)

@app.route('/login', methods=['POST'])
def login():
    print(request.form)
    if not Usuario.validar_login(request.form):
        print("login failed")
        return redirect('/')
    usuario_aceptado = Usuario.obtener_usuario_por_email(request.form)
    if usuario_aceptado == None:
        flash ("Email/Contraseña no válidos", "login")
        return redirect('/')
    session ['id_usuario'] = usuario_aceptado.id_usuario
    session ['nombre'] = usuario_aceptado.nombre
    return redirect('/home')