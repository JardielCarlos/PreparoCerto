from flask_restful import Resource, reqparse, marshal
from helpers.database import db
from model.proprietario import Proprietario 
from model.usuario import userFields
from helpers.logger import logger
from model.mensagem import Message, msgError
from sqlalchemy.exc import IntegrityError

parser = reqparse.RequestParser()

parser.add_argument("nome", type=str, help="Nome nao informado", required=True)
parser.add_argument("email", type=str, help="email nao informado", required=True)
parser.add_argument("senha", type=str, help="senha nao informado", required=True)

class Proprietarios(Resource):
  def get(self):
    logger.info("Proprietarios listados com Sucesso")
    return marshal(Proprietario.query.all(), userFields), 200
  
  def post(self):
    args = parser.parse_args()

    try:
      proprietario = Proprietario(args['nome'], args["email"], args['senha'])

      db.session.add(proprietario)
      db.session.commit()

      logger.info(f"Proprietario de id: {proprietario.id} criado com sucesso")
      return marshal(proprietario, userFields), 201
    
    except IntegrityError:
      codigo = Message(1, "Email ja cadastrado no sistema")
      return marshal(codigo, msgError)
    except:
      logger.error("Error ao cadastrar o Proprietario")

      codigo = Message(2, "Error ao cadastrar o Proprietario")
      return marshal(codigo, msgError), 400
  
class ProprietarioId(Resource):
  def get(self, id):
    proprietario = Proprietario.query.get(id)

    if proprietario is None:
      logger.error(f"Proprietario de id: {id} nao encontrado")

      codigo = Message(1, f"Proprietario de id: {id} nao encontrado")
      return marshal(codigo, msgError), 404
    
    logger.info(f"Proprietario de id: {proprietario.id} Listado com Sucesso")
    return marshal(proprietario, userFields), 200
  
  def put(self, id):
    args = parser.parse_args()

    try:
      userBd = Proprietario.query.get(id)

      if userBd is None:
        logger.error(f"Proprietario de id: {id} nao encontrado")

        codigo = Message(1, f"Proprietario de id: {id} nao encontrado")
        return marshal(codigo, msgError), 404
      
      userBd.nome = args["nome"]
      userBd.email = args["email"]
      userBd.senha = args["senha"]

      db.session.add(userBd)
      db.session.commit()
      
      logger.info(f"Proprietario de id: {id} atualizado com Sucesso")
      return marshal(userBd, userFields), 200
    
    except:
      logger.error("Error ao atualizar o Proprietario")

      codigo = Message(2, "Error ao atualizar o Proprietario")
      return marshal(codigo, msgError), 400
  
  def delete(self, id):

    userBd = Proprietario.query.get(id)

    if userBd is None:
      logger.error(f"Proprietario de id: {id} nao encontrado")

      codigo = Message(1, f"Proprietario de id: {id} nao encontrado")
      return marshal(codigo, msgError), 404

    db.session.delete(userBd)
    db.session.commit()
    
    logger.info(f"Proprietario de id: {id} deletado com sucesso")
    return {}, 200
