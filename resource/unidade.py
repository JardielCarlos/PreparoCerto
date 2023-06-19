from flask_restful import Resource, reqparse, marshal
from helpers.database import db
from helpers.logger import logger
from model.mensagem import Message, msgError

from model.unidade_medida import UnidadeMedida, unidadeFields

parser = reqparse.RequestParser()

parser.add_argument("sigla", type=str, help="sigla nao informada", required=True)

class Unidade(Resource):
    
  def get(self):
    logger.info("Unidades de medidas listadas com Sucesso")
    return marshal(UnidadeMedida.query.all(), unidadeFields), 200
  
  def post(self):
    args = parser.parse_args()

    try:
      unidade = UnidadeMedida(args['sigla'])

      db.session.add(unidade)
      db.session.commit()

      logger.info(f"unidade de medida de id: {unidade.id} criado com sucesso")
      return marshal(unidade, unidadeFields), 201
    except:
      logger.error("Error ao cadastrar a unidade de medida")

      codigo = Message(2, "Error ao cadastrar a unidade de medida")
      return marshal(codigo, msgError), 400
    
class UnidadeId(Resource):
  def get(self, id):
    logger.info(f"Unidade de medidade de id: {id} listado com sucesso")

    return marshal(UnidadeMedida.query.get(id), unidadeFields), 200

  def put(self, id):
    args = parser.parse_args()

    try:
      unidadeBd = UnidadeMedida.query.get(id)
      
      if unidadeBd is None:
        logger.error(f"Unidade de medida de id: {id} nao encontrado")

        codigo = Message(1, f"Unidade de medida de id: {id} nao encontrado")
        return marshal(codigo, msgError), 404
      
      unidadeBd.sigla = args["sigla"]

      db.session.add(unidadeBd)
      db.session.commit()

      logger.info(f"Unidade de medidade de id: {id} atualizado com sucesso")
      return marshal(unidadeBd, unidadeFields), 200
      
    except:
      logger.error("Erro ao atualizar a unidade de medida")

      codigo = Message(2, "Erro ao atualizar a unidade de medida")
      return marshal(codigo, msgError), 400
    
  def delete(self, id):
    unidadeBd = UnidadeMedida.query.get(id)

    if unidadeBd is None:
      logger.error(f"Unidade de medida de id: {id} nao encontrado")
      codigo = Message(1, f"Unidade de medida de id: {id} nao encontrado")
      return marshal(codigo, msgError)
    
    db.session.delete(unidadeBd)
    db.session.commit()

    logger.info(f"Unidade de medida de id: {id} deletado com sucesso")
    return {}, 200