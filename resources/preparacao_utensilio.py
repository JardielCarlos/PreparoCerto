from flask_restful import Resource, marshal, reqparse
from helpers.database import db
from helpers.logger import logger
from helpers.auth.token_verifier import token_verify

from model.mensagem import Message, msgFields
from model.preparacao_utensilio import PreparacaoUtensilio, utensilioPreparacaoTokenFields, utensiliosTokenFields
from model.utensilio import Utensilio
from model.preparacao import Preparacao

parser = reqparse.RequestParser()

parser.add_argument("utensilio", type=dict, help="Utensilio não informado", required=True)
parser.add_argument("preparacao", type=dict, help="Preparação não informada", required=True)


class UtensiliosPreparacao(Resource):
  @token_verify
  def get(self, tipo, refreshToken):
    if tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar os utensilios da preparacao")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

    preparacaoUtensilio = PreparacaoUtensilio.query.all()

    data = {'utensilioPreparacao': preparacaoUtensilio, 'token': refreshToken}

    logger.info("Preparação-Utensilios listados com sucesso")
    return marshal(data, utensilioPreparacaoTokenFields), 200

  @token_verify
  def post(self, tipo, refreshToken):
    if tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar os utensilios da preparacao")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

    args = parser.parse_args()

    utensilioId = args['utensilio']['id']
    preparacaoId = args['preparacao']['id']

    utensilioBd = Utensilio.query.get(utensilioId)
    preparacaoBd = Preparacao.query.get(preparacaoId)

    if utensilioBd is None:
      logger.error(f"Utensilio de id: {utensilioId} nao encontrado")

      codigo = Message(1, f"Utensilio de id: {utensilioId} não encontrado")
      return marshal(codigo, msgFields), 404

    if preparacaoBd is None:
      logger.error(f"Preparacao de id: {preparacaoId} nao encontrado")

      codigo = Message(1, f"Preparacao de id: {preparacaoId} não encontrado")
      return marshal(codigo, msgFields), 404

    utensilioPreparacao = PreparacaoUtensilio(utensilioBd, preparacaoBd)

    db.session.add(utensilioPreparacao)
    db.session.commit()

    data = {'utensilioPreparacao': utensilioPreparacao, 'token': refreshToken}

    logger.info(f"Preparação-Utensilio de id: {utensilioPreparacao.id} criado com sucesso")
    return marshal(data, utensilioPreparacaoTokenFields), 201

class UtensiliosPreparacaoId(Resource):
  @token_verify
  def get(self, tipo, refreshToken, id):
    if tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar os utensilios da preparacao")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

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

    data = {'utensilios': utensiliosPreparacao, 'token': refreshToken}

    logger.info(f"Todos os utensilios da preparação de id: {id} listados com sucesso")
    return marshal(data, utensiliosTokenFields), 200

  @token_verify
  def delete(self, tipo, refreshToken, id):
    if tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar os utensilios da preparacao")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

    preparacaoUtensilioBd = PreparacaoUtensilio.query.get(id)
    if preparacaoUtensilioBd is None:
      logger.error(f"UtensiliosPreparacao de id: {id} nao encontrado")

      codigo = Message(1, f"Utensilio da preparacao de id: {id} não encontrado")
      return marshal(codigo, msgFields), 404

    db.session.delete(preparacaoUtensilioBd)
    db.session.commit()

    logger.info(f"UtensiliosPreparacao de id: {id} deletado com sucesso")
    return {'token': refreshToken}, 200
