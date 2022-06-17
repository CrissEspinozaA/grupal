from flask_app.config.mysqlconnection import connectToMySQL 
from flask import flash
import re

class Sala:
    def __init__(self, data):
        self.id_sala = data["id_sala"]
        self.nombre_sala = data["nombre_sala"]
        self.descripcion = data["descripcion"]
        self.administrador = data["administrador"]
        self.mayor_edad = data["mayor_edad"]
        self.id_usuario = data["id_usuario"]

    @classmethod
    def muestra_salas(cls):
        query = "SELECT * FROM sala"
        mysql = connectToMySQL("grupal")
        results = mysql.query_db(query)
        salas = []
        for sala in results:
            salas.append(cls(sala))
        return salas

    @classmethod
    def crear_sala(cls, data):
        query = "INSERT INTO grupal.sala (nombre_sala, descripcion, administrador, mayor_edad, created_at, updated_at, id_usuario) VALUES (%(nombre_sala)s, %(descripcion)s, %(administrador)s, %(mayor_edad)s,  NOW(), NOW() ,%(id_usuario)s)"
        mysql = connectToMySQL("grupal")
        results = mysql.query_db(query, data)
        sala = {"sala.id_sala": results}
        return sala

    @classmethod
    def mostrar_sala(cls, data):
        query = "SELECT nombre_sala FROM sala WHERE id_usuario = %(id_usuario)s"
        mysql = connectToMySQL("grupal")
        result = mysql.query_db(query, data)
        if len(result) > 0:
            return cls(result[0])
        else:
            return None