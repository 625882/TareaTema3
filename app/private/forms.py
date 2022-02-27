from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from flask_wtf.file import FileRequired, FileAllowed, FileField
from wtforms.validators import DataRequired, Length, ValidationError
from PIL import Image
import os

class ClienteForm(FlaskForm):


    dni = StringField(label="DNI", validators=[
        DataRequired(message="El campo DNI es obligatorio"),
        Length(max=10, message="El campo DNI no tiene un formato válido.")
    ])

    nombre = StringField(label="Nombre", validators=[
        DataRequired(message="El campo nombre es obligatorio"),
        Length( max=20, message="El campo nombre debe ser entre 5 y 20 caracteres")
    ])

    apellidos = StringField(label="Apellidos", validators=[
        DataRequired(message="El campo apellidos es obligatorio"),
        Length(min=5, max=50, message="El campo apellidos debe ser entre 5 y 20 caracteres")
    ])

    imagen = FileField(label="Imagen", validators=[
        FileRequired(message="El campo imagen es obligatorio"),
        FileAllowed(['jpg','png'], message="Solo jpg y png")
    ])

    submit = SubmitField(label="Enviar")


    # Lo puse porque quería probar otra validación más y ya pues lo dejo
    def validate_dni(form,field):
        tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
        dig_ext = "XYZ"
        reemp_dig_ext = {'X': '0', 'Y': '1', 'Z': '2'}
        numeros = "1234567890"
        dni = form.dni.data
        if len(dni) == 9:
            dig_control = dni[8]
            dni = dni[:8]
            if dni[0] in dig_ext:
                dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
            if len(dni) != len([n for n in dni if n in numeros]) \
                   and tabla[int(dni) % 23] == dig_control:
                raise ValidationError("El DNI introducido no tiene formato válido " )
        else:
            raise ValidationError("El DNI introducido no es válido abajo")
