from flask_restful import Resource, marshal, reqparse
from helpers.database import db
from helpers.logger import logger

from model.cardapio import Cardapio,cardapioFields
from model.cardapio_preparacao import CardapioPreparacao
from model.mensagem import Message, msgFields
from model.empresa import Empresa

parser = reqparse.RequestParser()

parser.add_argument("empresa", type=dict, help="Empresa não informada", required=True)

class Cardapios(Resource):
  def get(self):
    cardapios = Cardapio.query.all()
    logger.info("Cardápios listados com sucesso")
    return marshal(cardapios, cardapioFields), 200

  def post(self):
    args = parser.parse_args()
    try:

      empresaId = args['empresa']['id']

      empresa = Empresa.query.get(empresaId)

      if empresa is None:
        logger.error(f"Empresa de id: {empresaId} não encontrada")

        codigo = Message(1, f"Empresa de id: {empresaId} não encontrada")
        return marshal(codigo, msgFields), 404

      cardapio = Cardapio(empresa)
      db.session.add(cardapio)
      db.session.commit()

      logger.info(f"Cardápio de id: {cardapio.id} criado com sucesso")
      return marshal(cardapio, cardapioFields), 201
    except:
      logger.error("Erro ao cadastrar o Cardápio")

      codigo = Message(2, "Erro ao cadastrar o Cardápio")
      return marshal(codigo, msgFields), 400

class CardapioId(Resource):
  def get(self, id):
    cardapio = Cardapio.query.get(id)

    if cardapio is None:
      logger.error(f"Cardápio de id: {id} não encontrado")

      codigo = Message(1, f"Cardápio de id: {id} não encontrado")
      return marshal(codigo, msgFields), 404

    logger.info(f"Cardápio de id: {id} listado com sucesso")
    return marshal(cardapio, cardapioFields), 200

  def delete(self, id):
    cardapioBd = Cardapio.query.get(id)
    cardapioPreparacaoBd = CardapioPreparacao.query.filter_by(cardapio_id=id)

    if cardapioBd is None:
      logger.error(f"Cardápio de id: {id} não encontrado")

      codigo = Message(1, f"Cardápio de id: {id} não encontrado")
      return marshal(codigo, msgFields), 404
    
    for i in cardapioPreparacaoBd:
        db.session.delete(i)

    db.session.delete(cardapioBd)
    db.session.commit()

    logger.info(f"Cardápio de id: {id} deletado com sucesso")
    return {}, 200
