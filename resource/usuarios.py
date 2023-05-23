from flask_restful import Resource, marshal, reqparse
from model.gestor import Gestor, gestorFields
from model.usuario import Usuario
from helpers.database import db

parser = reqparse.RequestParser()

parser.add_argument("nome", type=str, help="Nome não informado", required=True)
parser.add_argument("email", type=str, help="email não informado", required=True)
parser.add_argument("senha", type=str, help="senha não informado", required=True)

class Usuarios(Resource):
  def get(self):
    return marshal(Usuario.query.all(), gestorFields), 200
  
  def post(self):
    args = parser.parse_args()
    gestor = Gestor(args['nome'], args["email"], args['senha'])

    db.session.add(gestor)
    db.session.commit()

    return marshal(gestor, gestorFields), 201
