from flask_restful import Resource, reqparse
from models.partido import PartidoModel
class PartidoController(Resource):
    def get(self):
        partidos = PartidoModel.query.all()
        resultado = []
        for partido in partidos:
            resultado.append(partido.json())
        return {
            'success': True,
            'content': resultado,
            'message': None
        }