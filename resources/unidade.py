from flask_restful import Resource, reqparse, marshal
from helpers.database import db
from helpers.logger import logger
from model.mensagem import Message, msgFields
import datetime
from model.unidade_medida import UnidadeMedida, unidadeFields

parser = reqparse.RequestParser()

parser.add_argument("sigla", type=str, help="sigla não informada", required=True)

class Unidade(Resource):

  def get(self):
    unidadesMedida = UnidadeMedida.query.all()

    logger.info("Unidades de medida listadas com sucesso")
    return marshal(unidadesMedida, unidadeFields), 200

  def post(self):
    args = parser.parse_args()

    try:
      unidade = UnidadeMedida(args['sigla'])

      db.session.add(unidade)
      db.session.commit()

      logger.info(f"Unidade de medida de id: {unidade.id} criada com sucesso")
      return marshal(unidade, unidadeFields), 201
    except:
      logger.error("Error ao cadastrar a Unidade de medida")

      codigo = Message(2, "Error ao cadastrar a Unidade de medida")
      return marshal(codigo, msgFields), 400

class UnidadeId(Resource):
  def get(self, id):
    logger.info(f"Unidade de medidade de id: {id} listada com sucesso")

    return marshal(UnidadeMedida.query.get(id), unidadeFields), 200

  def put(self, id):
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

      logger.info(f"Unidade de medidade de id: {id} atualizada com sucesso")
      return marshal(unidadeBd, unidadeFields), 200

    except:
      logger.error("Erro ao atualizar a Unidade de medida")

      codigo = Message(2, "Erro ao atualizar a Unidade de medida")
      return marshal(codigo, msgFields), 400

  def delete(self, id):
    unidadeBd = UnidadeMedida.query.get(id)

    if unidadeBd is None:
      logger.error(f"Unidade de medida de id: {id} não encontrada")
      codigo = Message(1, f"Unidade de medida de id: {id} não encontrada")
      return marshal(codigo, msgFields)

    db.session.delete(unidadeBd)
    db.session.commit()

    logger.info(f"Unidade de medida de id: {id} deletada com sucesso")
    return {}, 200
