from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user

import app
from . import sesiones
from .forms import LoginForm
from .forms import UsuarioForm
from ..login.models import Usuario

PEEPER = "ClaveSecretaPeeper"

@app.login_manager.user_loader
def load_user(user_id):
    return Usuario.get_by_id(user_id)

@sesiones.route('/')
def index():
    return render_template('index.html')

@sesiones.route("/logoutsession/")
def logoutsession():
    logout_user()
    return redirect(url_for('sesiones.index'))

@sesiones.route("/welcome/")
def welcome():
    return render_template("welcome.html")

@sesiones.route("/altaUsuarioSesiones/", methods=["GET","POST"])
def altaUsuarioSesiones():
    if current_user.is_authenticated:
        return redirect(url_for("sesiones.welcome"))
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
            return redirect(url_for('sesiones.loginSesiones'))
        except Exception as e:
            error = "No se ha podido dar de alta " + e.__str__()
            app.logger.error(error)
    return render_template("altaUsuarioSesiones.html", form=form, error=error)

@sesiones.route("/loginSesiones/", methods=["GET","POST"])
def loginSesiones():
    if current_user.is_authenticated:
        return redirect(url_for("private.indexcliente"))
    error = ""
    form = LoginForm(request.form)
    if form.validate_on_submit():
        username = form.username.data
        password = PEEPER + form.password.data
        usuario = Usuario.get_by_username(username)

        if usuario and usuario.check_password(password):
            login_user(usuario, form.recuerdame.data)
            return redirect(url_for("private.indexcliente"))
        else:
            error = "Usuario y/o contraseña incorrecta"
            app.logger.warning("Se ha intentado iniciar sesión con el usuario: "+username)
    return render_template("loginSesiones.html", form=form, error=error)

