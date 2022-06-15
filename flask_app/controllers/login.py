from flask_app import app 
from flask_app.models.users import User
from flask_bcrypt import Bcrypt

from flask import render_template, request, redirect, url_for, session, flash 
bcrypt = Bcrypt(app)

@app.route('/') # crea una ruta
def users(): # crea una función
    return render_template('users.html') # devulve el template users.html

@app.route('/dashboard') 
def dashboard():
    if 'user.id' in session:
        usuarios = User.get_all_users()
        print(usuarios)
        return render_template('dashboard.html', usuarios = usuarios)
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
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }
    User.save_user(data)
    logged_user = User.get_user_by_email(request.form)
    session ['user.id'] = logged_user.id
    session ['user.first_name'] = logged_user.first_name
    session ['user.last_name'] = logged_user.last_name
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
    session ['user.id'] = logged_user.id
    session ['user.first_name'] = logged_user.first_name
    session ['user.last_name'] = logged_user.last_name
    return redirect('/dashboard')