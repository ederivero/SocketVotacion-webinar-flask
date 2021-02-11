from config.sqlalchemy import bd
from datetime import datetime


class VotoModel(bd.Model):
    __tablename__ = 't_voto'
    voto_id = bd.Column(type_=bd.Integer, primary_key=True,
                        autoincrement=True, nullable=False, unique=True)
    voto_fecha = bd.Column(type_=bd.DateTime(), nullable=False, default=datetime.now())
    # RELATIONS
    partido = bd.Column(bd.ForeignKey('t_partido.partido_id'),
                        name='partido_id', type_=bd.Integer,  nullable=False)
    votante = bd.Column(bd.ForeignKey('t_votante.votante_dni'),
                        name='votante_dni', type_=bd.String(9),  nullable=False)

    def __init__(self, partido, votante):
        self.partido = partido
        self.votante = votante

    def json(self):
        return {
            'id': self.voto_id,
            'voto_fecha': self.voto_fecha,
            'partido': self.partidoVotos.partido_nombre,
            'votante': self.votanteVotos.votante_dni
        }

    def save(self):
        bd.session.add(self)
        bd.session.commit()
        bd.session.close()
