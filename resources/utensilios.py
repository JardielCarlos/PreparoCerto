from flask_restful import Resource, marshal, reqparse
from helpers.logger import logger
from helpers.database import db
from helpers.auth.token_verifier import token_verify

from model.utensilio import Utensilio, utensilioTokenFields
from model.mensagem import Message, msgFields

parser = reqparse.RequestParser()

parser.add_argument("nome", type=str, help="nome não informada", required=True)

class Utensilios(Resource):
  @token_verify
  def get(self, tipo, refreshToken):
    if tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar os utensilios")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

    utensilios = Utensilio.query.all()

    data = {"utensilio": utensilios, 'token': refreshToken}

    logger.info("Utensilios listados com sucesso")
    return marshal(data, utensilioTokenFields), 200
  @token_verify
  def post(self, tipo, refreshToken):
    if tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar os utensilios")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

    args = parser.parse_args()

    try:
      utensilio = Utensilio(args["nome"])

      db.session.add(utensilio)
      db.session.commit()

      data = {"utensilio": utensilio, 'token': refreshToken}

      logger.info(f"Utensilio de id: {utensilio.id} criado com sucesso")
      return marshal(data, utensilioTokenFields), 201
    except:
      logger.error("Error ao cadastrar Utensilio")

      codigo = Message(2, "Error ao cadastrar Utensilio")
      return marshal(codigo, msgFields), 400

class UtensilioId(Resource):
  @token_verify
  def get(self, tipo, refreshToken, id):
    if tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar os utensilios")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403
    utensilio = Utensilio.query.get(id)
    if utensilio is None:
      logger.error(f"Utensilio de id : {id} não encontrado")

      codigo = Message(1, f"Utensilio de id : {id} não encontrado")
      return marshal(codigo, msgFields), 404

    logger.info(f"Utensilio de id: {id} listado com sucesso")

    data = {"utensilio": utensilio, 'token': refreshToken}
    return marshal(data, utensilioTokenFields), 200
  @token_verify
  def put(self, tipo, refreshToken, id):
    if tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar os utensilios")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

    args = parser.parse_args()

    try:
      utensilioBd = Utensilio.query.get(id)

      if utensilioBd is None:
        logger.error(f"Utensilio de id: {id} nao encontrado")
        codigo = Message(1, f"Utensilio de id: {id} nao encontrado")

        return marshal(codigo, msgFields), 404
      utensilioBd.nome = args["nome"]

      db.session.add(utensilioBd)
      db.session.commit()

      data = {"utensilio": utensilioBd, 'token': refreshToken}

      logger.info(f"Utensilio de id: {id} atualizado com sucesso")
      return marshal(data, utensilioTokenFields), 200
    except:
      logger.error("Error ao atualizar utensilio")

      codigo = Message(2, "Error ao atualizar utensilio")
      return marshal(codigo, msgFields)
  @token_verify
  def delete(self, tipo, refreshToken, id):
    if tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar os utensilios")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

    utensilioBd = Utensilio.query.get(id)

    if utensilioBd is None:
      logger.info(f"Utensilio de id: {id} nao encontrado")

      codigo = Message(1, f"Utensilio de id: {id} nao encontrado")
      return marshal(codigo, msgFields)

    db.session.delete(utensilioBd)
    db.session.commit()

    logger.info(f"Utensilio de id: {id} deletado com sucesso")
    return {'token': refreshToken}, 200
