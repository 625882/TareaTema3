import base64

from flask import render_template, request, redirect, url_for
from sqlalchemy import text
from werkzeug.datastructures import CombinedMultiDict

from . import login
from .forms import LoginForm
from .forms import UsuarioForm
from .models import Usuario

PEEPER = "ClaveSecretaPeeper"

@login.route('/')
def index():  # put application's code here
    return render_template('index.html')

@login.route("/welcome/")
def welcome():
    return render_template("welcome.html")

@login.route("/altaUsuario/", methods=["GET","POST"])
def altaUsuario():
    error = ""
    form = UsuarioForm(request.form)
    if form.validate_on_submit():
        try:
            usuario = Usuario()
            usuario.username = form.username.data
            password = PEEPER + form.password.data
            usuario.set_password(password)
            usuario.nombre = form.nombre.data
            usuario.apellidos = form.apellidos.data
            usuario.create()
            return redirect(url_for('login.welcome'))
        except Exception as e:
            error = "No se ha podido dar de alta " + e.__str__()
    return render_template("altaUsuario.html", form=form, error=error)

@login.route("/loginHashPeeper/", methods=["GET","POST"])
def loginHashPeeper():
    error = ""
    form = LoginForm(request.form)
    if form.validate_on_submit():
        username = form.username.data
        password = PEEPER + form.password.data
        usuario = Usuario.get_by_username(username)

        if usuario and usuario.check_password(password):
            return redirect(url_for("login.indexcliente"))
        else:
            error = "Usuario y/o contraseña incorrecta"
    return render_template("loginHashPeeper.html", form=form, error=error)