from config.sqlalchemy import bd

class PartidoModel(bd.Model):
    __tablename__='t_partido'
    partido_id = bd.Column(type_=bd.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    partido_nombre = bd.Column(type_=bd.String(255), nullable=False, unique=True)
    partido_img_partido = bd.Column(type_=bd.String(255), nullable=False, unique=True)
    partido_img_candidato = bd.Column(type_=bd.String(255), nullable=False, unique=True)
    partido_nombre_candidato = bd.Column(type_=bd.String(255), nullable=False, unique=True)
    # INVERSE RELATION 
    partido_votos = bd.relationship('VotoModel', backref = 'partidoVotos')

    def __init__(self, nombre, img_partido, img_candidato, nombre_candidato):
        self.partido_nombre = nombre
        self.partido_img_partido = img_partido
        self.partido_img_candidato = img_candidato
        self.partido_nombre_candidato = nombre_candidato
    
    def json(self):
        return {
            'id': self.partido_id,
            'partido_nombre': self.partido_nombre,
            'partido_img_partido': self.partido_img_partido,
            'partido_img_candidato': self.partido_img_candidato,
            'partido_nombre_candidato': self.partido_nombre_candidato
        }
    
    def save(self):
        bd.session.add(self)
        bd.session.commit()
        bd.session.close()
