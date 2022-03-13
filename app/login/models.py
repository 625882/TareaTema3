from sqlalchemy.exc import IntegrityError
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    nombre = db.Column(db.String(20), nullable=False)
    apellidos = db.Column(db.String(50), nullable=False)

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            raise Exception("Error: ya existe un usuario con el mismo username")

    def __str__(self):
        return self.apellidos + ', ' + self.nombre

    @staticmethod
    def get_by_id(id):
        return Usuario.query.get(id)

    @staticmethod
    def get_by_username(username):
        return Usuario.query.filter_by(username=username).first()

    def set_password(self, password):
        method = "pbkdf2:sha256:260000"
        self.password = generate_password_hash(password, method=method)

    def check_password(self, password):
        return check_password_hash(self.password, password)
