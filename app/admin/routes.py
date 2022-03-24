from flask import render_template, abort
from flask_login import login_required, current_user

from . import admin
from ..auth.decorator import admin_required
from ..login.models import Usuario


@admin.route('/adminindex/')
@login_required
@admin_required
def adminindex():
    usuarios = Usuario.query.all()

    return render_template("adminindex.html", usuarios=usuarios)