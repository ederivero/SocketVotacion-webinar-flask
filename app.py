from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from config.sqlalchemy import bd

# import the models
from models.partido import PartidoModel
from models.votante import VotanteModel
from models.voto import VotoModel

app = Flask(__name__)
cors = CORS(app)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:root@localhost:3306/webinarflask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

@app.before_first_request
def create_tables():
    bd.init_app(app)
    bd.drop_all(app=app)
    bd.create_all(app=app)

@app.route('/')
def base_url():
    return 'Bienvenido a mi API 🙃'


if __name__ == '__main__':
    app.run(debug=True)
