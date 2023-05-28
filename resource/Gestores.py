from flask_restful import Resource, reqparse, marshal
from helpers.database import db
from model.gestor import Gestor
from model.usuario import userFields
from helpers.logger import logger
from model.mensagem import Message, msgError

parser = reqparse.RequestParser()

parser.add_argument("nome", type=str, help="Nome nao informado", required=True)
parser.add_argument("email", type=str, help="email nao informado", required=True)
parser.add_argument("senha", type=str, help="senha nao informado", required=True)

class Gestores(Resource):
  def get(self):
    logger.info("Gestores listados com Sucesso")
    return marshal(Gestor.query.all(), userFields), 200
  
  def post(self):
    args = parser.parse_args()

    try:
      gestor = Gestor(args['nome'], args["email"], args['senha'])

      db.session.add(gestor)
      db.session.commit()

      logger.info(f"Gestor de id: {gestor.id} criado com sucesso")
      return marshal(gestor, userFields), 201
    except:
      logger.error("Error ao cadastrar o Gestor")

      codigo = Message(2, "Error ao cadastrar o Gestor")
      return marshal(codigo, msgError), 400
  
class GestorId(Resource):
  def get(self, id):
    gestor = Gestor.query.get(id)

    if gestor is None:
      logger.error(f"Gestor de id: {id} nao encontrado")

      codigo = Message(1, f"Gestor de id: {id} nao encontrado")
      return marshal(codigo, msgError), 404
    
    logger.info(f"Gestor de id: {gestor.id} Listado com Sucesso")
    return marshal(gestor, userFields), 200
  
  def put(self, id):
    args = parser.parse_args()

    try:
      userBd = Gestor.query.get(id)

      if userBd is None:
        logger.error(f"Gestor de id: {id} nao encontrado")

        codigo = Message(1, f"Gestor de id: {id} nao encontrado")
        return marshal(codigo, msgError), 404
      
      userBd.nome = args["nome"]
      userBd.email = args["email"]
      userBd.senha = args["senha"]

      db.session.add(userBd)
      db.session.commit()
      
      logger.info(f"Gestor de id: {id} atualizado com Sucesso")
      return marshal(userBd, userFields), 200
    
    except:
      logger.error("Error ao atualizar o Gestor")

      codigo = Message(2, "Error ao atualizar o Gestor")
      return marshal(codigo, msgError), 400
  
  def delete(self, id):

    userBd = Gestor.query.get(id)

    if userBd is None:
      logger.error(f"Gestor de id: {id} nao encontrado")

      codigo = Message(1, f"Gestor de id: {id} nao encontrado")
      return marshal(codigo, msgError), 404

    db.session.delete(userBd)
    db.session.commit()
    
    logger.info(f"Gestor de id: {id} deletado com sucesso")
    return {}, 200