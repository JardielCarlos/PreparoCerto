from flask_restful import Resource, marshal, reqparse
from model.preparador import Preparador, preparadorFields
from helpers.database import db
from helpers.logger import logger
from model.mensagem import Message, msgError
from sqlalchemy.exc import IntegrityError
from model.empresa import Empresa

parser = reqparse.RequestParser()

parser.add_argument("nome", type=str, help="Nome nao informado", required=True)
parser.add_argument("email", type=str, help="Email nao informado", required=True)
parser.add_argument("senha", type=str, help="Senha nao informado", required=True)
parser.add_argument("empresa", type=dict, help="Empresa nao informado", required=True)

class Preparadores (Resource):
  def get(self):
    logger.info("Preparadores listados com sucesso")
    return marshal(Preparador.query.all(), preparadorFields), 200
  
  def post(self):
    args = parser.parse_args()
    try:
      empresaId = args['empresa']
      empresa = Empresa.query.get(empresaId)
      if empresa is None:
        logger.error(f"Empresa de id: {empresaId} nao encontrado")

        codigo = Message(1, f"Empresa de id: {empresaId} nao encontrado")
        return marshal(codigo, msgError), 404

      preparador = Preparador(args['nome'], args['email'], args['senha'], empresa)

      db.session.add(preparador)
      db.session.commit()

      logger.info(f"Preparador de id: {preparador.id} criado com sucesso")
      return marshal(preparador, preparadorFields), 201
    
    except IntegrityError:
      codigo = Message(1, "Email ja cadastrado no sistema")
      return marshal(codigo, msgError)
    except:
      logger.error("Erro ao cadastrar o preparador")

      codigo = Message(2, "Erro ao cadastrar o preparador")
      return marshal(codigo, msgError), 400
    
class PreparadorId(Resource):
  def get(self, id):
    preparador = Preparador.query.get(id)

    if preparador is None:
      logger.error(f"Preparador de id: {id} nao encontrado")

      codigo = Message(1, f"Preparador de id: {id} nao encontrado")
      return marshal(codigo, msgError), 404
    
    logger.info(f"Preparador de id: {id} listado com sucesso")
    return marshal(preparador, preparadorFields), 200
  
  def put(self, id):
    args = parser.parse_args()

    try:
      userBd = Preparador.query.get(id)
      if userBd is None:
        logger.error(f"Prepador de id: {id} nao encontrado")

        codigo = Message(1, f"Preparador de id: {id} nao encontrado")
        return marshal(codigo, msgError), 404
      
      userBd.nome = args['nome']
      userBd.email = args['email']
      userBd.senha = args['senha']

      db.session.add(userBd)
      db.session.commit()

      logger.info(f"Preparador de id: {id} atualizado com sucesso")
      return marshal(userBd, preparadorFields)
    except:
      logger.error("Erro ao atualizar o Preparador")

      codigo = Message(2, "Erro ao atualizar o Preparador")
      return marshal(codigo, msgError), 400
    
  def delete(self, id):
    userBd = Preparador.query.get(id)

    if userBd is None:
      logger.error(f"Preparador de id: {id} nao encontrado")

      codigo = Message(1, f"Preparador de id: {id} nao encontrado")
      return marshal(codigo, msgError), 404

    db.session.delete(userBd)
    db.session.commit()

    logger.info(f"Preparador de id: {id} deletado com sucesso")
    return {}, 200