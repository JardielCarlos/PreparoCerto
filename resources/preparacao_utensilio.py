from flask_restful import Resource, marshal, reqparse
from helpers.database import db
from helpers.logger import logger

from model.mensagem import Message, msgFields

from model.preparacao_utensilio import PreparacaoUtensilio, utensilioPreparacaoFields, utensiliosFields
from model.utensilio import Utensilio
from model.preparacao import Preparacao

parser = reqparse.RequestParser()

parser.add_argument("utensilio", type=dict, help="Utensilio não informado", required=True)
parser.add_argument("preparacao", type=dict, help="Preparação não informada", required=True)


class UtensiliosPreparacao(Resource):
  def get(self):
    logger.info("Preparação-Utensilios listados com sucesso")
    return marshal(PreparacaoUtensilio.query.all(), utensilioPreparacaoFields), 200

  def post(self):
    args = parser.parse_args()

    utensilioId = args['utensilio']['id']
    preparacaoId = args['preparacao']['id']

    if utensilioId is None:
      logger.error(f"Utensilio de id: {utensilioId} nao encontrado")

      codigo = Message(1, f"Utensilio de id: {utensilioId} não encontrado")
      return marshal(codigo, msgFields), 404
    if preparacaoId is None:
      logger.error(f"Preparacao de id: {preparacaoId} nao encontrado")

      codigo = Message(1, f"Preparacao de id: {preparacaoId} não encontrado")
      return marshal(codigo, msgFields), 404

    utensilioBd = Utensilio.query.get(utensilioId)
    preparacaoBd = Preparacao.query.get(preparacaoId)

    utensilioPreparacao = PreparacaoUtensilio(utensilioBd, preparacaoBd)

    db.session.add(utensilioPreparacao)
    db.session.commit()

    logger.info(f"Preparação-Utensilio de id: {utensilioPreparacao.id} criado com sucesso")
    return marshal(utensilioPreparacao, utensilioPreparacaoFields), 201

class UtensiliosPreparacaoId(Resource):
  def get(self, id):
    utensiliosPreparacao = PreparacaoUtensilio.query.filter_by(preparacao_id=id).all()
    preparacao = Preparacao.query.get(id)
    utensilios = Utensilio.query.get(id)

    if preparacao is None:
      logger.error(f"Preparação de id: {id} não encontrada")
      codigo = Message(1, f"Preparação de id: {id} não encontrada")

      return marshal(codigo, msgFields), 404
    elif utensilios == []:
      logger.error("Não existe nenhum utensílio cadastrado")
      codigo = Message(1, "Não existe nenhum utensílio cadastrado")

      return marshal(codigo, msgFields), 404
    elif utensiliosPreparacao == []:
      logger.error(f"A preparação de id: {id} não possui utensilios cadastrados")
      codigo = Message(1, f"A preparação de id: {id} não possui utensilios cadastrados")

      return marshal(codigo, msgFields), 404

    logger.info(f"Todos os utensilios da preparação de id: {id} listados com sucesso")
    return marshal(utensiliosPreparacao, utensiliosFields), 200

  def delete(self, id):
    preparacaoUtensilioBd = PreparacaoUtensilio.query.get(id)
    if preparacaoUtensilioBd is None:
      logger.error(f"UtensiliosPreparacao de id: {id} nao encontrado")

      codigo = Message(1, f"Utensilio da preparacao de id: {id} não encontrado")
      return marshal(codigo, msgFields), 404

    db.session.delete(preparacaoUtensilioBd)
    db.session.commit()

    logger.info(f"UtensiliosPreparacao de id: {id} deletado com sucesso")
    return {}, 200
