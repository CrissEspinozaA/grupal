from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

class Usuario: 
    def __init__(self, data): 
        self.id_usuario = data["id_usuario"]
        self.nombre = data["nombre"]
        self.apellido = data["apellido"]
        self.edad = data["edad"]
        self.email = data["email"]
        self.apodo = data["apodo"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        
    @staticmethod 
    def validar_usuario(usuario):
        is_valid = True
        if len(usuario["nombre"]) < 2:
            flash("El nombre debe tener más de 2 caracteres", "register")
            is_valid = False
        if len(usuario["apellido"]) < 2:
            flash("El apellido debe tener más de 2 caracteres", "register")
            is_valid = False
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.fullmatch(regex, usuario["email"]):
            flash("El email no es válido", "register")
            is_valid = False
        return is_valid


    @staticmethod 
    def validar_login(usuario):
        # print(usuario)
        is_valid = True
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b' 
        if not re.fullmatch(regex, usuario["email"]):
            flash("El Email no es válido", "register")
            is_valid = False
        if len(usuario["user_password"]) < 8:
            flash("La contraseña debe tener más de 8 caracteres", "register")
            is_valid = False
        return is_valid
        
    
    @classmethod 
    def guardar_ususario(cls, data):
        query = "INSERT INTO usuario (nombre, apellido, edad, email, apodo, password, created_at, updated_at) VALUES (%(nombre)s, %(apellido)s, %(edad)s, %(email)s, %(apodo)s, %(password)s, NOW(), NOW())"
        mysql = connectToMySQL("mydb")
        results = mysql.query_db(query, data)
        usuario = {"usuario.id_usuario": results}
        return usuario

    @classmethod
    def obtener_usuario_por_email(cls, data):
        query = "SELECT * FROM usuario WHERE email = %(email)s"
        mysql = connectToMySQL("mydb")
        result = mysql.query_db(query, data)
        if len(result) > 0:
            return cls(result[0])
        else:
            return None