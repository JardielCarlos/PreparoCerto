from flask_restful import Resource, marshal, reqparse
from helpers.database import db
from helpers.logger import logger
from helpers.auth.token_verifier import token_verify

from model.cardapio import Cardapio, cardapioTokenFields
from model.mensagem import Message, msgFields
from model.empresa import Empresa

parser = reqparse.RequestParser()

parser.add_argument("empresa", type=dict, help="Empresa não informada", required=True)

class Cardapios(Resource):
  @token_verify
  def get(self, tipo, refreshToken):
    if tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar o cardapio")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

    cardapios = Cardapio.query.all()

    data = {'cardapio': cardapios, 'token': refreshToken}

    logger.info("Cardápios listados com sucesso")
    return marshal(data, cardapioTokenFields), 200

  @token_verify
  def post(self, tipo, refreshToken):
    if tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar o cardapio")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403
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

      data = {'cardapio': cardapio, 'token': refreshToken}

      logger.info(f"Cardápio de id: {cardapio.id} criado com sucesso")
      return marshal(data, cardapioTokenFields), 201
    except:
      logger.error("Erro ao cadastrar o Cardápio")

      codigo = Message(2, "Erro ao cadastrar o Cardápio")
      return marshal(codigo, msgFields), 400

class CardapioId(Resource):
  @token_verify
  def get(self, tipo, refreshToken, id):
    if tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar o cardapio")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

    cardapio = Cardapio.query.get(id)

    if cardapio is None:
      logger.error(f"Cardápio de id: {id} não encontrado")

      codigo = Message(1, f"Cardápio de id: {id} não encontrado")
      return marshal(codigo, msgFields), 404

    data = {'cardapio': cardapio, 'token': refreshToken}

    logger.info(f"Cardápio de id: {id} listado com sucesso")
    return marshal(data, cardapioTokenFields), 200

  @token_verify
  def delete(self, tipo, refreshToken, id):
    if tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar o cardapio")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

    cardapioBd = Cardapio.query.get(id)

    if cardapioBd is None:
      logger.error(f"Cardápio de id: {id} não encontrado")

      codigo = Message(1, f"Cardápio de id: {id} não encontrado")
      return marshal(codigo, msgFields), 404

    db.session.delete(cardapioBd)
    db.session.commit()

    logger.info(f"Cardápio de id: {id} deletado com sucesso")
    return {'token': refreshToken}, 200
