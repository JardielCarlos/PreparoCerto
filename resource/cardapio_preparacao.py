from flask_restful import Resource, marshal, reqparse
from helpers.database import db
from helpers.logger import logger
from model.mensagem import Message, msgError

from model.cardapio_preparacao import CardapioPreparacao, cardapioPreparacaoFields
from model.cardapio import Cardapio
from model.preparacao import Preparacao

parser = reqparse.RequestParser()

parser.add_argument("cardapio",  type=dict, help="Cardápio não informado", required=True)
parser.add_argument("preparacao",  type=dict, help="Preparação não informada", required=True)

class CardapioPreparacoes(Resource):
  def get(self):
    return marshal(CardapioPreparacao.query.all(), cardapioPreparacaoFields), 200
  
  def post(self):
    args = parser.parse_args()

    try:
      cardapio = Cardapio.query.get(args["cardapio"]['id'])
      preparacao = Preparacao.query.get(args["preparacao"]['id'])

      if cardapio is None:
        logger.error("Cardápio não encontrado")

        codigo = Message(1, "Cardápio não encontrado")
        return marshal(codigo, msgError), 404
      
      elif preparacao is None:
        logger.error("Preparação não encontrada")

        codigo = Message(1, "Preparação não encontrada")
        return marshal(codigo, msgError), 404
      
      cardapioPreparacao = CardapioPreparacao(cardapio, preparacao)

      db.session.add(cardapioPreparacao)
      db.session.commit()

      logger.info(f"Cardápio-Preparação de id: {cardapioPreparacao.id} criada com sucesso")
      return marshal(cardapioPreparacao, cardapioPreparacaoFields), 200
    
    except:
      logger.error(f"Error ao cadastrar o Cardápio-Preparação")

      codigo = Message(2, "Error ao cadastrar o Cardápio-Preparação")
      return marshal(codigo, msgError), 400
  
class CardapioPreparacaoId(Resource):
  def get(self, id):
    cardapioPreparacao = CardapioPreparacao.query.get(id)
    if cardapioPreparacao is None:
      logger.error(f"Cardápio-Preparação de id: {id} nao informado")

      codigo = Message(1, f"Cardápio-Preparação de id: {id} nao informado")
      return marshal(codigo, msgError), 404
    
    return marshal(cardapioPreparacao, cardapioPreparacaoFields),200

  def put(self, id):
    args = parser.parse_args()

    try:
      cardapioPreparacaoBd = CardapioPreparacao.query.get(id)
      
      cardapioId = args["cardapio"]["id"]
      preparacaoId = args["preparacao"]["id"]

      cardapio = Cardapio.query.get(cardapioId)
      preparacao = Preparacao.query.get(preparacaoId)

      if cardapioPreparacaoBd is None:
        logger.error(f"Cardápio-Preparação de id: {id} nao encontrado")

        codigo = Message(1, f"Cardápio-Preparação de id: {id} nao encontrado")
        return marshal(codigo, msgError), 404
      
      elif cardapio is None:
        logger.error(1, f"Cardápio de id: {id} não encontrado")
        
        codigo = Message(1, f"Cardápio de id: {id} não encontrado")
        return marshal(codigo, msgError), 404
      
      elif preparacao is None:
        logger.error(1, f"Preparação de id: {id} não encontrada")

        codigo = Message(1, f"Preparação de id: {id} não encontrada")
        return marshal(codigo, msgError), 404
      

      cardapioPreparacaoBd.cardapio = cardapio
      cardapioPreparacaoBd.preparacao = preparacao

      db.session.add(cardapioPreparacaoBd)
      db.session.commit()

      logger.info(f"Cardápio-Preparação de id: {id} atualizada com sucesso")
      return marshal(cardapioPreparacaoBd, cardapioPreparacaoFields), 200
    except:
      logger.error("Erro ao atualizar o Cardápio-Preparação")

      codigo = Message(2, "Erro ao atualizar o Cardápio-Preparação")
      return marshal(codigo, msgError), 400
    
  def delete(self, id):
    cardapioPreparacao = CardapioPreparacao.query.get(id)

    if cardapioPreparacao is None:
      logger.error(f"Cardápio-Preparação de id: {id} não encontrado")

      codigo = Message(1, f"Cardápio-Preparação de id: {id} não encontrado")
      return marshal(codigo, msgError), 404

    db.session.add(cardapioPreparacao)
    db.session.commit()

    logger.info(f"Cardápio-Preparação de id: {id} deletado com sucesso")
    return {}, 200