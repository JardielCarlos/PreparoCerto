from flask_restful import Resource, reqparse, marshal
from helpers.database import db
from model.gestor import Gestor, gestorFields
parser = reqparse.RequestParser()

parser.add_argument("nome", type=str, help="Nome não informado", required=True)
parser.add_argument("email", type=str, help="email não informado", required=True)
parser.add_argument("senha", type=str, help="senha não informado", required=True)

class Gestores(Resource):
  def get(self):
    return marshal(Gestor.query.all(), gestorFields), 200
  
  def post(self):
    args = parser.parse_args()
    gestor = Gestor(args['nome'], args["email"], args['senha'])

    db.session.add(gestor)
    db.session.commit()

    return marshal(gestor, gestorFields), 201
