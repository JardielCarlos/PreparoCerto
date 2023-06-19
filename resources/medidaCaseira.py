from flask_restful import Resource, reqparse, marshal
from helpers.database import db
from helpers.logger import logger
from model.mensagem import Message, msgError

from model.medida_caseira import MedidaCaseira, medidaCaseiraFields

parser = reqparse.RequestParser()

parser.add_argument("quantidade", type=str, help="Quantidade não informada", required=True)
parser.add_argument("descricao", type=str, help="Descricao não informada", required=True)

class MedidasCaseiras(Resource):
    
    def get(self):
      logger.info("Medidas caseiras listada com sucesso")
      return marshal(MedidaCaseira.query.all(), medidaCaseiraFields), 200
    
    def post(self):
      args = parser.parse_args()

      try:
        medida = MedidaCaseira(args['quantidade'], args['descricao'])

        db.session.add(medida)
        db.session.commit()

        logger.info(f"Medida Caseira de id: {medida.id} criada com sucesso")
        return marshal(medida, medidaCaseiraFields), 201
      except:
        logger.error("Error ao cadastrar a Medida Caseira")

        codigo = Message(2, "Error ao cadastrar a Medida Caseira")
        return marshal(codigo, msgError), 400

class MedidaCaseiraId(Resource):
  def get(self, id):
    logger.info(f"Medida Caseira de id: {id} listada com sucesso")

    return marshal(MedidaCaseira.query.get(id), medidaCaseiraFields), 200
  
  def put(self, id):
    args = parser.parse_args()

    try:
      medidaBd = MedidaCaseira.query.get(id)

      if medidaBd is None:
        logger.error(f"Medida Caseira de id: {id} não encontrada")

        codigo = Message(1, f"Medida Caseira de id: {id} não encontrada")
        return marshal(codigo, msgError), 404
      
      medidaBd.quantidade = args["quantidade"]
      medidaBd.descricao = args["descricao"]

      db.session.add(medidaBd)
      db.session.commit()

      logger.info(f"Medida caseira de id: {id} atualizada com sucesso")
      return marshal(medidaBd, medidaCaseiraFields), 200
    except:
      logger.error("Erro ao atualizar a Medida Caseira")
      codigo = Message(2, "Erro ao atualizar a Medida Caseira")
      return marshal(codigo, msgError)
    
  def delete(self, id):
    medidaBd = MedidaCaseira.query.get(id)
    
    if medidaBd is None:
      logger.error(f"Medida Caseira de id: {id} não encontrada")
      codigo = Message(1, f"Medida Caseira de id: {id} não encontrada")
      return marshal(codigo, msgError), 404
    
    db.session.delete(medidaBd)
    db.session.commit()

    logger.info(f"Medida Caseira de id: {id} deletada com sucesso")
    return {}, 200