from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
#Establecemos la cadena de conexión
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/tareaTema3Project'
#Desactivamos la gestión de notificaciones de SQLAlchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Instanciamos un objeto de la clase SQLAlchemy
db = SQLAlchemy(app)
#Instanciamos un objeto de la clase migrate.
migrate = Migrate(app,db)
app.secret_key = "clave_secreta"

from .public import public
from .private import private

def create_app():
    app.register_blueprint(public)
    app.register_blueprint(private)
    return  app