from flask_restful import Resource, marshal, reqparse
from helpers.database import db
from helpers.logger import logger
from model.mensagem import Message, msgFields

from model.cardapio_preparacao import CardapioPreparacao, cardapioPreparacaoFields, preparacoesFields
from model.cardapio import Cardapio
from model.preparacao import Preparacao

parser = reqparse.RequestParser()

parser.add_argument("cardapio",  type=dict, help="Cardápio não informado", required=True)
parser.add_argument("preparacao",  type=dict, help="Preparação não informada", required=True)

class CardapioPreapracoes(Resource):
  def get(self):
    cardapioPreparacao = CardapioPreparacao.query.all()
    cardapios = Cardapio.query.all()
    preparacoes = Preparacao.query.all()

    if cardapios == []:
      logger.error("Não existe nenhum cardapio cadastrado")
      codigo = Message(1, "Não existe nenhum cardapio cadastrado")

      return marshal(codigo, msgFields), 404
    elif preparacoes == []:
      logger.error("Não existe nenhuma preparação cadastrada")
      codigo = Message(1, "Não existe nenhuma preparação cadastrada")

      return marshal(codigo, msgFields), 404
    elif cardapioPreparacao == []:
      logger.error("Não existe nenhum relacionamento Cardápio-Preparação cadastrado")
      codigo = Message(1, "Não existe nenhum relacionamento Cardápio-Preparação cadastrado")

      return marshal(codigo, msgFields), 404

    logger.info("Todos os cardápios e suas preparações listados com sucesso")
    return marshal(cardapioPreparacao, cardapioPreparacaoFields), 200

  def post(self):
    args = parser.parse_args()

    try:
      cardapio = Cardapio.query.get(args["cardapio"]['id'])
      preparacao = Preparacao.query.get(args["preparacao"]['id'])

      if cardapio is None:
        logger.error("Cardápio não encontrado")

        codigo = Message(1, "Cardápio não encontrado")
        return marshal(codigo, msgFields), 404

      elif preparacao is None:
        logger.error("Preparação não encontrada")

        codigo = Message(1, "Preparação não encontrada")
        return marshal(codigo, msgFields), 404

      cardapioPreparacao = CardapioPreparacao(cardapio, preparacao)

      db.session.add(cardapioPreparacao)
      db.session.commit()

      logger.info(f"Cardápio-Preparação de id: {cardapioPreparacao.id} criada com sucesso")
      return marshal(cardapioPreparacao, cardapioPreparacaoFields), 200

    except:
      logger.error(f"Error ao cadastrar o Cardápio-Preparação")

      codigo = Message(2, "Error ao cadastrar o Cardápio-Preparação")
      return marshal(codigo, msgFields), 400

class CardapioPreapracaoId(Resource):
  def get(self, id):
    cardapio = Cardapio.query.get(id)
    preparacoes = CardapioPreparacao.query.filter_by(cardapio_id=id).all()

    if cardapio is None:
      logger.error(f"Cardápio de id: {id} não encontrado")

      codigo = Message(1, f"Cardápio de id: {id} não encontrado")
      return marshal(codigo, msgFields), 404

    elif preparacoes == []:
      logger.error(f"O cardápio de id: {id} não possui preparações cadastradas")

      codigo = Message(1, f"O cardápio de id: {id} não possui preparações cadastradas")
      return marshal(codigo, msgFields), 404

    return marshal(preparacoes, preparacoesFields), 200

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
        return marshal(codigo, msgFields), 404

      elif cardapio is None:
        logger.error(1, f"Cardápio de id: {id} não encontrado")

        codigo = Message(1, f"Cardápio de id: {id} não encontrado")
        return marshal(codigo, msgFields), 404

      elif preparacao is None:
        logger.error(1, f"Preparação de id: {id} não encontrada")

        codigo = Message(1, f"Preparação de id: {id} não encontrada")
        return marshal(codigo, msgFields), 404


      cardapioPreparacaoBd.cardapio = cardapio
      cardapioPreparacaoBd.preparacao = preparacao

      db.session.add(cardapioPreparacaoBd)
      db.session.commit()

      logger.info(f"Cardápio-Preparação de id: {id} atualizada com sucesso")
      return marshal(cardapioPreparacaoBd, cardapioPreparacaoFields), 200
    except:
      logger.error("Erro ao atualizar o Cardápio-Preparação")

      codigo = Message(2, "Erro ao atualizar o Cardápio-Preparação")
      return marshal(codigo, msgFields), 400

  def delete(self, id):
    cardapioPreparacao = CardapioPreparacao.query.get(id)

    if cardapioPreparacao is None:
      logger.error(f"Cardápio-Preparação de id: {id} não encontrado")

      codigo = Message(1, f"Cardápio-Preparação de id: {id} não encontrado")
      return marshal(codigo, msgFields), 404

    db.session.delete(cardapioPreparacao)
    db.session.commit()

    logger.info(f"Cardápio-Preparação de id: {id} deletado com sucesso")
    return {}, 200
