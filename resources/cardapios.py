from flask_restful import Resource, marshal, reqparse
from model.cardapio import Cardapio,cardapioFields
from helpers.database import db
from helpers.logger import logger
from model.mensagem import Message, msgError
from model.empresa import Empresa

parser = reqparse.RequestParser()

parser.add_argument("nome", type=str, help="Nome nao informado", required=True)
parser.add_argument("empresa", type=dict, help="empresa nao informado", required=True)

class Cardapios(Resource):
  def get(self):
    logger.info("Cardapios listados com sucesso")
    return marshal(Cardapio.query.all(), cardapioFields), 200
  
  def post(self):
    args = parser.parse_args()
    try:

      empresaId = args['empresa']['id']

      empresa = Empresa.query.get(empresaId)
      
      if empresa is None:
        logger.error(f"Empresa de id: {empresaId} nao encontrado")
        
        codigo = Message(1, f"Empresa de id: {empresaId} nao encontrado")
        return marshal(codigo, msgError), 404

      cardapio = Cardapio(args['nome'], empresa)
      db.session.add(cardapio)
      db.session.commit()

      logger.info(f"Cardapio de id: {cardapio.id} criado com sucesso")
      return marshal(cardapio, cardapioFields), 201
    except:
      logger.error("Erro ao cadastrar o cardapio")

      codigo = Message(2, "Erro ao cadastrar o cardapio")
      return marshal(codigo, msgError), 400
    
class CardapioId(Resource):
  def get(self, id):
    cardapio = Cardapio.query.get(id)

    if cardapio is None:
      logger.error(f"Cardapio de id: {id} nao encontrado")

      codigo = Message(1, f"Cardapio de id: {id} nao encontrado")
      return marshal(codigo, msgError), 404
    
    logger.info(f"Cardapior de id: {id} listado com sucesso")
    return marshal(cardapio, cardapioFields), 200
  
  def put(self, id):
    args = parser.parse_args()

    try:
      cardapioBd = Cardapio.query.get(id)
      if cardapioBd is None:
        logger.error(f"Cardapio de id: {id} nao encontrado")

        codigo = Message(1, f"Cardapio de id: {id} nao encontrado")
        return marshal(codigo, msgError), 404
      
      cardapioBd.nome = args['nome']

      db.session.add(cardapioBd)
      db.session.commit()

      logger.info(f"Cardapio de id: {id} atualizado com sucesso")
      return marshal(cardapioBd, cardapioFields)
    except:
      logger.error("Erro ao atualizar o Cardapio")

      codigo = Message(2, "Erro ao atualizar o Cardapio")
      return marshal(codigo, msgError), 400
    
  def delete(self, id):
    cardapioBd = Cardapio.query.get(id)

    if cardapioBd is None:
      logger.error(f"Cardapio de id: {id} nao encontrado")

      codigo = Message(1, f"Cardapio de id: {id} nao encontrado")
      return marshal(codigo, msgError), 404

    db.session.delete(cardapioBd)
    db.session.commit()

    logger.info(f"Cardapio de id: {id} deletado com sucesso")
    return {}, 200