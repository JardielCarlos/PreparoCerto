from flask_restful import Resource, reqparse, marshal
from helpers.database import db
from helpers.logger import logger
from sqlalchemy.exc import IntegrityError
from helpers.auth.token_verifier import token_verify

from model.mensagem import Message, msgFields
from model.medida_caseira import MedidaCaseira, medidaCaseiraTokenFields

parser = reqparse.RequestParser()

parser.add_argument("quantidade", type=int, help="Quantidade não informada", required=True)
parser.add_argument("descricao", type=str, help="Descricao não informada", required=True)

class MedidasCaseiras(Resource):
  @token_verify
  def get(self, tipo, refreshToken):
    if tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar as medidas caseira")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

    medidasCseiras = MedidaCaseira.query.all()

    data ={'medidaCaseira': medidasCseiras, 'token': refreshToken}

    logger.info("Medidas caseiras listada com sucesso")
    return marshal(data, medidaCaseiraTokenFields), 200

  @token_verify
  def post(self, tipo, refreshToken):
    if tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar as medidas caseira")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

    args = parser.parse_args()

    try:
      if args['quantidade'] <= 0:
        logger.error("Quantidade nao informada")

        codigo = Message(1, "Quantidade nao informada")
        return marshal(codigo, msgFields), 400

      if len(args['descricao']) == 0:
        logger.error("descricao nao informado")

        codigo = Message(1, "descricao nao informado")
        return marshal(codigo, msgFields), 400

      medida = MedidaCaseira(args['quantidade'], args['descricao'])

      db.session.add(medida)
      db.session.commit()

      data ={'medidaCaseira': medida, 'token': refreshToken}

      logger.info(f"Medida Caseira de id: {medida.id} criada com sucesso")
      return marshal(data, medidaCaseiraTokenFields), 201
    except:
      logger.error("Error ao cadastrar a Medida Caseira")

      codigo = Message(2, "Error ao cadastrar a Medida Caseira")
      return marshal(codigo, msgFields), 400

class MedidaCaseiraId(Resource):
  @token_verify
  def get(self, tipo, refreshToken, id):
    if tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar as medidas caseira")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

    medida = MedidaCaseira.query.get(id)

    data ={'medidaCaseira': medida, 'token': refreshToken}

    logger.info(f"Medida Caseira de id: {id} listada com sucesso")
    return marshal(data, medidaCaseiraTokenFields), 200

  @token_verify
  def put(self, tipo, refreshToken, id):
    if tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar as medidas caseira")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

    args = parser.parse_args()

    try:
      medidaBd = MedidaCaseira.query.get(id)

      if medidaBd is None:
        logger.error(f"Medida Caseira de id: {id} não encontrada")

        codigo = Message(1, f"Medida Caseira de id: {id} não encontrada")
        return marshal(codigo, msgFields), 404

      medidaBd.quantidade = args["quantidade"]
      medidaBd.descricao = args["descricao"]

      db.session.add(medidaBd)
      db.session.commit()

      data ={'medidaCaseira': medidaBd, 'token': refreshToken}


      logger.info(f"Medida caseira de id: {id} atualizada com sucesso")
      return marshal(data, medidaCaseiraTokenFields), 200
    except:
      logger.error("Erro ao atualizar a Medida Caseira")
      codigo = Message(2, "Erro ao atualizar a Medida Caseira")
      return marshal(codigo, msgFields)

  @token_verify
  def delete(self, tipo, refreshToken, id):
    if tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar as medidas caseira")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403
    try:
      medidaBd = MedidaCaseira.query.get(id)

      if medidaBd is None:
        logger.error(f"Medida Caseira de id: {id} não encontrada")
        codigo = Message(1, f"Medida Caseira de id: {id} não encontrada")
        return marshal(codigo, msgFields), 404

      db.session.delete(medidaBd)
      db.session.commit()

      logger.info(f"Medida Caseira de id: {id} deletada com sucesso")
      return {'token': refreshToken}, 200

    except IntegrityError:
      logger.error(f"Medida Caseira de id: {id} nao pode ser deletado possui dependencias com preparacao_ingrediente")

      codigo = Message(1, f"Medida Caseira de id: {id} nao pode ser deletado possui dependencias com preparacao_ingrediente")
      return marshal(codigo, msgFields), 400
