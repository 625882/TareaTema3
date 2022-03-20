from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, ValidationError


class LoginForm(FlaskForm):
    username = StringField(label="Nombre de usuario", validators=[
        DataRequired(message="El nombre de usuario es obligatorio"),
        Length(max=20, message="El nombre de usuario no puede ser superior a 20 caracteres")
    ])

    password = PasswordField(label="Contraseña", validators=[
        DataRequired(message="La contraseña es obligatoria"),
        Length(min=8, message="La contraseña no puede ser inferior a 8 caracteres")
    ])

    recuerdame = BooleanField(label="Recuerdame")

class UsuarioForm(FlaskForm):

    username = StringField(label="Nombre de usuario", validators=[
        DataRequired(message="El nombre de usuario es obligatorio"),
        Length(max=20, message="El nombre de usuario no puede ser superior a 20 caracteres")
    ])

    password = PasswordField(label="Contraseña", validators=[
        DataRequired(message="La contraseña es obligatoria"),
        Length(min=8, message="La contraseña no puede ser inferior a 8 caracteres")
    ])

    passwordRepeat = PasswordField(label="Repita la contraseña", validators=[
        DataRequired(message="La repetición de la contraseña es obligatoria"),
        Length(min=8, message="La contraseña no puede ser inferior a 8 caracteres")
    ])

    nombre = StringField(label="Nombre", validators=[
        DataRequired(message="El nombre es obligatorio"),
        Length(max=20, message="El nombre no puede ser superior a 10 caracteres")
        ])

    apellidos = StringField(label="Apellidos", validators=[
        DataRequired(message="Los apellidos son obligatorio"),
        Length(max=50, message="Los apellidos no pueden superar los 50 caracteres")
        ])

    # submit = SubmitField(label="Dar de alta")

    def validate_password(form,field):
        if not password_check(form.password.data):
            raise ValidationError("La contraseña no cumple el formato. Debe tener al menos un dígito, mayúsculas, minúsculas y caráteres especiales.")
        if field.data != form.passwordRepeat.data:
            raise ValidationError("No coinciden las contraseñas")

    def validate_passwordRepeat(form, field):
        if field.data != form.password.data:
            raise ValidationError("No coinciden las contraseñas")

def password_check(passwd):

    SpecialSym = ['#', '$', '%', '&']
    val = True

    if not any(char.isdigit() for char in passwd):
        val = False

    if not any(char.isupper() for char in passwd):
        val = False

    if not any(char.islower() for char in passwd):
        val = False

    if not any(char in SpecialSym for char in passwd):
        val = False

    return val