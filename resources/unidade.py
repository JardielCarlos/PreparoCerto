from flask_restful import Resource, reqparse, marshal
from helpers.database import db
from helpers.logger import logger
from helpers.auth.token_verifier import token_verify
from sqlalchemy.exc import IntegrityError

from model.mensagem import Message, msgFields
from model.unidade_medida import UnidadeMedida, unidadeTokenFields

parser = reqparse.RequestParser()

parser.add_argument("sigla", type=str, help="sigla não informada", required=True)

class Unidade(Resource):
  @token_verify
  def get(self, tipo, refreshToken):
    if tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar as unidades de medida")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

    unidadesMedida = UnidadeMedida.query.all()

    data = {'unidade': unidadesMedida, 'token': refreshToken}

    logger.info("Unidades de medida listadas com sucesso")
    return marshal(data, unidadeTokenFields), 200
  @token_verify
  def post(self, tipo, refreshToken):
    if tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar as unidades de medida")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

    args = parser.parse_args()

    try:
      unidade = UnidadeMedida(args['sigla'])

      db.session.add(unidade)
      db.session.commit()

      data = {'unidade': unidade, 'token': refreshToken}

      logger.info(f"Unidade de medida de id: {unidade.id} criada com sucesso")
      return marshal(data, unidadeTokenFields), 201
    except:
      logger.error("Error ao cadastrar a Unidade de medida")

      codigo = Message(2, "Error ao cadastrar a Unidade de medida")
      return marshal(codigo, msgFields), 400

class UnidadeId(Resource):
  @token_verify
  def get(self, tipo, refreshToken, id):
    if tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar as unidades de medida")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

    unidade = UnidadeMedida.query.get(id)
    if unidade is None:
      logger.error(f"Unidade de id: {id} nao encontrado")

      codigo = Message(1, f"Unidade de id: {id} não encontrado!")
      return marshal(codigo, msgFields), 404

    data = {'unidade': unidade, 'token': refreshToken}

    logger.info(f"Unidade de medidade de id: {id} listada com sucesso")

    return marshal(data, unidadeTokenFields), 200

  @token_verify
  def put(self, tipo, refreshToken, id):
    if tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar as unidades de medida")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

    args = parser.parse_args()

    try:
      unidadeBd = UnidadeMedida.query.get(id)

      if unidadeBd is None:
        logger.error(f"Unidade de medida de id: {id} não encontrada")

        codigo = Message(1, f"Unidade de medida de id: {id} não encontrada")
        return marshal(codigo, msgFields), 404

      unidadeBd.sigla = args["sigla"]

      db.session.add(unidadeBd)
      db.session.commit()

      data = {'unidade': unidadeBd, 'token': refreshToken}

      logger.info(f"Unidade de medidade de id: {id} atualizada com sucesso")
      return marshal(data, unidadeTokenFields), 200

    except:
      logger.error("Erro ao atualizar a Unidade de medida")

      codigo = Message(2, "Erro ao atualizar a Unidade de medida")
      return marshal(codigo, msgFields), 400

  @token_verify
  def delete(self, tipo, refreshToken, id):
    if tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar as unidades de medida")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

    try:
      unidadeBd = UnidadeMedida.query.get(id)

      if unidadeBd is None:
        logger.error(f"Unidade de medida de id: {id} não encontrada")
        codigo = Message(1, f"Unidade de medida de id: {id} não encontrada")
        return marshal(codigo, msgFields)

      db.session.delete(unidadeBd)
      db.session.commit()

      logger.info(f"Unidade de medida de id: {id} deletada com sucesso")
      return {'token': refreshToken}, 200
    except IntegrityError:
      logger.error(f"Unidade de medida de id: {id} nao pode ser deletada ela possui dependencia com preparacao_ingrediente")

      codigo = Message(1, f"Unidade de medida de id: {id} nao pode ser deletada ela possui dependencia com a preparacao do ingrediente")
      return marshal(codigo, msgFields), 400
