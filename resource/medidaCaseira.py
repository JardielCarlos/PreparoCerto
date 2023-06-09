from flask_restful import Resource, reqparse, marshal
from helpers.database import db
from helpers.logger import logger
from model.mensagem import Message, msgError

from model.medida_caseira import MedidaCaseira, medidaCaseiraFields

parser = reqparse.RequestParser()

parser.add_argument("quantidade", type=str, help="quantidade nao informada", required=True)
parser.add_argument("descricao", type=str, help="descricao nao informada", required=True)

class MedidasCaseiras(Resource):
    
    def get(self):
      # logger.info("Proprietarios listados com Sucesso")

      return marshal(MedidaCaseira.query.all(), medidaCaseiraFields), 200
    
    def post(self):
      args = parser.parse_args()

      try:
        medida = MedidaCaseira(args['quantidade'], args['descricao'])

        db.session.add(medida)
        db.session.commit()

        logger.info(f"MedidaCaseira de id: {medida.id} criado com sucesso")
        return marshal(medida, medidaCaseiraFields), 201
      except:
        logger.error("Error ao cadastrar o MedidaCaseira")

        codigo = Message(2, "Error ao cadastrar o MedidaCaseira")
        return marshal(codigo, msgError), 400

