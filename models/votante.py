from config.sqlalchemy import bd
from datetime import datetime, timedelta

class VotanteModel(bd.Model):
    __tablename__ = 't_votante'
    votante_dni = bd.Column(type_=bd.String(8), primary_key=True, nullable=False, unique=True)
    votante_email = bd.Column(type_=bd.String(
        255), nullable=False, unique=True)
    votante_nombre = bd.Column(type_=bd.String(
        255), nullable=False, unique=True)
    votante_apellido = bd.Column(
        type_=bd.String(255), nullable=False, unique=True)
    votante_fechavencimiento = bd.Column(type_=bd.DateTime(), nullable=False, default=False)
    votante_hash = bd.Column(type_=bd.String(255), nullable=False)
    # INVERSE RELATION 
    votante_votos = bd.relationship('VotoModel', backref='votanteVotos')

    def __init__(self,dni, email, nombre, apellido, hash):
        self.votante_dni = dni
        self.votante_email = email
        self.votante_nombre = nombre
        self.votante_apellido = apellido
        self.votante_fechavencimiento = datetime.now() + timedelta(minutes=30) - timedelta(hours=5)
        self.votante_hash = hash

    def json(self):
        return {
            'dni': self.votante_dni,
            'votante_email': self.votante_email,
            'votante_nombre': self.votante_nombre,
            'votante_apellido': self.votante_apellido
        }

    def save(self):
        bd.session.add(self)
        bd.session.commit()
    
    def __str__(self):
        return self.votante_dni