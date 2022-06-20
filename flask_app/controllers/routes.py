from flask_app import app 
from flask_app.models.users import User
from flask_app.models.salas import Sala
from flask_bcrypt import Bcrypt

from flask import render_template, request, redirect, url_for, session, flash 
bcrypt = Bcrypt(app)

@app.route('/') # crea una ruta
def users(): # crea una función
    return render_template('login.html') # devulve el template users.html

@app.route('/dashboard') 
def dashboard():
    if 'user.id_usuario' in session:
        salas = Sala.muestra_salas()
        print(salas)
        print("muestro las salas")
        return render_template('dashboard.html', salas = salas)
    else:
        return redirect('/')

@app.route('/user') 
def userRegister():
    if 'user.id_usuario' in session:
        user = User.get_all_users()
        print(user)
        return render_template('register.html')
    else:
        return redirect('/')

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect('/')

@app.route('/register', methods=['POST'])
def register():
    print(request.form)
    if not User.validate_user(request.form):
        return redirect('/user')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "nombre": request.form['nombre'],
        "apellido": request.form['apellido'],
        "apodo": request.form['apodo'],
        "edad": request.form['edad'],
        "email": request.form['email'],
        "password": pw_hash
    }
    User.save_user(data)
    logged_user = User.get_user_by_email(request.form)
    session ['user.id_usuario'] = logged_user.id_usuario
    session ['user.nombre'] = logged_user.nombre
    session ['user.apellido'] = logged_user.apellido
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    print(request.form)
    if not User.validate_login(request.form):
        print("login failed")
        return redirect('/')
    logged_user = User.get_user_by_email(request.form)
    if logged_user == None:
        flash ("Email/Contraseña no válidos", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(logged_user.password, request.form['password']):
        flash ("Email/Contraseña no válidos", "login")
        return redirect('/')
    session ['user.id_usuario'] = logged_user.id_usuario
    session ['user.nombre'] = logged_user.nombre
    session ['user.apellido'] = logged_user.apellido
    return redirect('/dashboard')



@app.route('/login_chat', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if(request.method=='POST'):
        username = request.form['username']
        room = request.form['room']
        #Store the data in session
        session['username'] = username
        session['room'] = room
        return render_template('chat.html', session = session)
    else:
        if(session.get('username') is not None):
            return render_template('chat.html', session = session)
        else:
            return redirect(url_for('index'))

@app.errorhandler(404) 
def url_error(e):
    return "Página no encontrada", 404

