from flask_restful import Resource, reqparse, marshal
from helpers.database import db
from model.gestor import Gestor
from model.usuario import userFields
parser = reqparse.RequestParser()

parser.add_argument("nome", type=str, help="Nome não informado", required=True)
parser.add_argument("email", type=str, help="email não informado", required=True)
parser.add_argument("senha", type=str, help="senha não informado", required=True)

class Gestores(Resource):
  def get(self):
    return marshal(Gestor.query.all(), userFields), 200
  
  def post(self):
    args = parser.parse_args()
    gestor = Gestor(args['nome'], args["email"], args['senha'])

    db.session.add(gestor)
    db.session.commit()

    return marshal(gestor, userFields), 201
  
class GestorId(Resource):
  def get(self, idUser):
    gestor = Gestor.query.get(idUser)
    return marshal(gestor, userFields), 200
  
  def put(self, idUser):
    args = parser.parse_args()

    userBd = Gestor.query.get(idUser)

    userBd.nome = args["nome"]
    userBd.email = args["email"]
    userBd.senha = args["senha"]

    db.session.add(userBd)
    db.session.commit()
    
    return marshal(userBd, userFields), 200
  
  def delete(self, idUser):

    useBd = Gestor.query.get(idUser)

    db.session.delete(useBd)
    db.session.commit()

    return {}, 200