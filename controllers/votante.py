from flask_restful import Resource, reqparse
from models.votante import VotanteModel
from config.utils import buscarPersona, sendMail
import uuid
class VotanteController(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'votante_email',
            required=True,
            type=str,
            help='Falta el votante_email',
            location='json'
        )
        parser.add_argument(
            'votante_dni',
            required=True,
            type=int,
            help='Falta el votante_dni',
            location='json'
        )
        parser.add_argument(
            'votante_verificacion',
            required=True,
            type=int,
            help='Falta el votante_verificacion',
            location='json'
        )
        args = parser.parse_args()
        persona = buscarPersona(args['votante_dni'])
        try:
            if persona['success']:
                if(persona['data']['codigo_verificacion']== args['votante_verificacion']):
                    hash = uuid.uuid4().hex
                    votante = VotanteModel(args['votante_dni'],  args['votante_email'], persona['data']['nombres'], persona['data']['apellido_paterno']+' '+persona['data']['apellido_materno'], hash)
                    votante.save()
                    if sendMail(votante.votante_email, persona['data']['nombre_completo'], hash):
                        return {
                            'success': True,
                            'content': votante.json(),
                            'message': 'Se creo el votante, que revise su correo para votar'
                        }, 201
                    else:
                        return {
                            'success': False,
                            'content': None,
                            'message': 'Error al enviar el correo, vuelva a intentarlo mas tarde'
                        }, 500
                else:
                    return {
                        'success': False,
                        'content': None,
                        'message': 'Error codigo de verificacion'
                    }, 500        
            return {
                'success': False,
                'content': None,
                'message': 'Error dni incorrecto'
            }, 500
        except Exception as e :
            print(e)
            return {
                'success': False,
                'content': None,
                'message': 'Error usuario duplicado DNI ya existe'
            }, 500
