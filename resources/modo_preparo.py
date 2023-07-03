from flask_restful import Resource, reqparse, marshal
from helpers.database import db
from helpers.logger import logger
from helpers.auth.token_verifier import token_verify

from model.mensagem import Message, msgFields
from model.preparacao import Preparacao
from model.modo_preparo import ModoPreparo, modoPreparoTokenFields

parser = reqparse.RequestParser()

parser.add_argument("text", type=str, help="text nao informada", required=True)
parser.add_argument("preparacao", type=dict, help="preparacao nao informada", required=False)

class ModosPreparo(Resource):
  @token_verify
  def get(self, tipo, refreshToken):
    if tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar o modo de preparo")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

    modosPreparo = ModoPreparo.query.order_by(ModoPreparo.criacao).all()

    logger.info("ModosPreparo listados com sucesso")

    data = {'modoPreparo': modosPreparo, 'token': refreshToken}

    return marshal(data, modoPreparoTokenFields), 200

  @token_verify
  def post(self, tipo, refreshToken):
    if tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar o modo de preparo")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

    args = parser.parse_args()
    try:
      preparacaoId = args["preparacao"]["id"]

      preparacao = Preparacao.query.get(preparacaoId)
      if preparacao is None:
        codigo = Message(1, f"preparacao de id: {preparacaoId} não encontrado")
        return marshal(codigo, msgFields), 404

      modoPreparo = ModoPreparo(args['text'], preparacao)

      db.session.add(modoPreparo)
      db.session.commit()

      data = {"modoPreparo": modoPreparo, 'token': refreshToken}

      logger.info(f"Modo Preparo de id: {modoPreparo.id} criado com sucesso")
      return marshal(data, modoPreparoTokenFields), 201

    except KeyError:
      logger.error("Id da preparacao não informado")
      codigo = Message(1, f"Id da preparacao não informado")
      return marshal(codigo, msgFields), 400

    except TypeError:
      logger.error("Preparacao nao informado")
      codigo = Message(1, "Preparacao nao informado")
      return marshal(codigo, msgFields), 400

    except:
      logger.error("Error ao cadastrar Modo de preparo")

      codigo = Message(2, "Error ao cadastrar Modo de preparo")
      return marshal(codigo, msgFields), 400

class ModosPreparoId(Resource):
  @token_verify
  def get(self, tipo, refreshToken, id):
    if tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar o modo de preparo")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

    modopreparo = ModoPreparo.query.filter_by(preparacao_id=id).order_by(ModoPreparo.criacao).all()

    if modopreparo is None:
      logger.error(f"Preparacao de id: {id} nao encontrada")

      codigo = Message(1, f"Preparacao de id: {id} nao encontrada")
      return marshal(codigo, msgFields), 404

    data = {"modoPreparo": modopreparo, 'token': refreshToken}

    logger.info(f"Preparacao de id: {id} listada com sucesso")
    return marshal(data, modoPreparoTokenFields), 200

  @token_verify
  def put(self, tipo, refreshToken, id):
    if tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar o modo de preparo")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

    args = parser.parse_args()

    try:
      modoPreparoBd = ModoPreparo.query.get(id)

      if modoPreparoBd is None:
        logger.error(f"Modo de preparo de id: {id} nao encontrado")

        codigo = Message(1, f"Modo de preparo de id: {id} nao encontrado")
        return marshal(codigo, msgFields), 404

      modoPreparoBd.text = args["text"]

      db.session.add(modoPreparoBd)
      db.session.commit()

      data = {"modoPreparo": modoPreparoBd, 'token': refreshToken}

      logger.info(f"Modo de preparo de id: {id} atualizado com sucesso")
      return marshal(data, modoPreparoTokenFields), 200
    except:
      logger.error("Erro ao atualizar Modo de preparo")
      codigo = Message(2, "Erro ao atualizar Modo de preparo")
      return marshal(codigo, msgFields)

  @token_verify
  def delete(self, tipo, refreshToken, id):
    if tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar o modo de preparo")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403
    modoPreparoBd = ModoPreparo.query.get(id)

    if modoPreparoBd is None:
      logger.error(f"Modo de preparo de id: {id} nao encontrado")
      codigo = Message(1, f"Modo de preparo de id: {id} nao encontrado")
      return marshal(codigo, msgFields), 404

    db.session.delete(modoPreparoBd)
    db.session.commit()

    logger.info(f"Modo de preparo de id: {id} deletado com sucesso")
    return {'token': refreshToken}, 200
