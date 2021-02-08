from flask import Flask, request
from flask_restful import Api
from flask_cors import CORS
from config.sqlalchemy import bd
from datetime import datetime
from flask_socketio import SocketIO, send, emit
# import the models
from models.partido import PartidoModel
from models.votante import VotanteModel
from models.voto import VotoModel
from sqlalchemy import *
from sqlalchemy.orm.session import sessionmaker
#import the controllers
from controllers.votante import VotanteController

app = Flask(__name__)
cors = CORS(app)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI']='mysql://b5h52w8xbsbsnkuh:hj0wkhdba46mjywj@z5zm8hebixwywy9d.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/u2wup6o8i6s68pxg'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['SECRET_KEY'] = 'webinar'
socketio = SocketIO(app, cors_allowed_origins ='*')


def obtain_session():
    """ Get SQLAlchemy session """
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    session = sessionmaker()
    # Bind the sessionmaker to engine
    session.configure(bind=engine)
    return session()

@app.before_first_request
def create_tables():
    bd.init_app(app)
    # bd.drop_all(app=app)
    bd.create_all(app=app)

@app.route('/')
def base_url():
    return 'Bienvenido a mi API 🙃'

@app.route('/votante')
def validar_votante():
    id = request.args.get('id',None)
    if id:
        votante = VotanteModel.query.filter_by(votante_hash=id).first()
        if (votante is not None):
            if (datetime.now() > votante.votante_fechavencimiento):
                return {
                    'success': False,
                    'content': None,
                    'message': 'Hash caducado'
                }, 500    
            else:
                voto = VotoModel.query.filter_by(votante= votante.votante_dni).first()
                if voto:
                    return {
                        'success': False,
                        'content': None,
                        'message': 'Votante ya votó'
                    }, 500    
                else:
                    partidos = PartidoModel.query.all()
                    resultado = []
                    for partido in partidos:
                        resultado.append(partido.json())
                    return {
                        'success': True,
                        'content': resultado,
                        'message': None
                    }, 200
        else:
            return {
                'success': False,
                'content': None,
                'message': 'Hash no corresponde'
            }, 500
    return {
        'success': False,
        'content': None,
        'message': 'Falta el id del votante'
    }, 500

@app.route('/voto', methods=['POST'])
def registrar_voto():
    hash = request.get_json().get('hash', None)
    partido = request.get_json().get('partido', None)
    if hash and partido:
        votante = VotanteModel.query.filter_by(votante_hash=hash).first()
        voto = VotoModel(partido, votante)
        voto.save()
        sess = obtain_session()
        # devolver los resultados de los votos
        result = sess.query(VotoModel.partido, func.count(VotoModel.partido).label('count')).group_by(VotoModel.partido).all()
        elecciones = []
        for partido in result:
            partido_nombre = PartidoModel.query.filter_by(partido_id=partido[0]).first().partido_nombre
            elecciones.append({
                'partido_nombre':partido_nombre,
                'votos': partido[1]
            })
        socketio.emit('votos',elecciones)
        return {
            'success': True,
            'content': voto.json(),
            'message': 'Se registro exitosamente el voto'
        }, 201
    else:
        return {
            'success': False,
            'content': None,
            'message': 'Faltan datos en el body'
        }, 500

api.add_resource(VotanteController, '/registro')

if __name__ == '__main__':
    socketio.run(app, debug=True)
    # app.run(debug=True)
