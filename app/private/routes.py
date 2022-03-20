import base64

from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user
from werkzeug.datastructures import CombinedMultiDict

from . import private
from .forms import ClienteForm
from .models import Cliente


@private.route("/indexcliente/", methods=["GET","POST"])
def indexcliente():
    if not current_user.is_authenticated:
        return redirect(url_for("login.loginHashPeeper"))
    clientes = Cliente.query.all()

    return render_template("indexcliente.html", clientes = clientes)

@private.route("/altaCliente/", methods=["GET","POST"])
def altaCliente():
    if not current_user.is_authenticated:
        return redirect(url_for("login.loginHashPeeper"))
    form = ClienteForm(CombinedMultiDict((request.files, request.form)))
    if form.validate_on_submit():
        dni = request.form.get("dni")
        nombre = request.form.get("nombre")
        apellidos = request.form.get("apellidos")

        encoded_bytes = base64.b64encode(form.imagen.data.read())

        if  len(encoded_bytes) > 1024*1024:
            form.imagen.errors.append("Tamaño máximo 1MB")
            return render_template("altaUsuarioSesiones.html", form =  form)
        else:
            encoded_string = str(encoded_bytes).replace("b'", "").replace("'", "")
            cliente = Cliente()
            cliente.dni = dni
            cliente.nombre = nombre
            cliente.apellidos = apellidos
            cliente.imagen = encoded_string
            cliente.save()
            clientes = Cliente.query.all()

        return render_template("indexcliente.html", clientes=clientes)

    return render_template("altaUsuarioSesiones.html", form = form)