from sqlalchemy.exc import IntegrityError
from app import db
class Cliente(db.Model):
    dni = db.Column(db.String(10),primary_key=True)
    nombre = db.Column(db.String(20),nullable=False)
    apellidos = db.Column(db.String(50))
    imagen = db.Column(db.String())

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            raise Exception("Error: ya existe un cliente con el mismo DNI")
