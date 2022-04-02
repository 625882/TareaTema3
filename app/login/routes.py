from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user

import app
from . import login
from .forms import LoginForm
from .forms import UsuarioForm
from .models import Usuario

PEEPER = "ClaveSecretaPeeper"

@app.login_manager.user_loader
def load_user(user_id):
    return Usuario.get_by_id(user_id)

@login.route('/')
def index():  # put application's code here
    return render_template('index.html')

@login.route("/welcome/")
def welcome():
    return render_template("welcome.html")

@login.route("/altaUsuario/", methods=["GET","POST"])
def altaUsuario():
    if current_user.is_authenticated:
        return redirect(url_for("login.welcome"))
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
            app.logger.info("Se ha dado de alta el usuario: "+usuario.username)
            return redirect(url_for('login.welcome'))
        except Exception as e:
            error = "No se ha podido dar de alta " + e.__str__()
            app.logger.error(error)
    return render_template("altaUsuarioSesiones.html", form=form, error=error)

@login.route("/loginHashPeeper/", methods=["GET","POST"])
def loginHashPeeper():
    if current_user.is_authenticated:
        return redirect(url_for("login.indexcliente"))
    error = ""
    form = LoginForm(request.form)
    if form.validate_on_submit():
        username = form.username.data
        password = PEEPER + form.password.data
        usuario = Usuario.get_by_username(username)
        if app.recaptcha.verify():
            if usuario and usuario.check_password(password):
                app.logger.info("Ha accedido el usuario: " + usuario.username)
                return redirect(url_for("login.indexcliente"))
            else:
                error = "Usuario y/o contraseña incorrecta"
                app.logger.error(error)
        else:
            error = "Captcha incorrecto. Eres un robot."
    return render_template("loginSesiones.html", form=form, error=error)