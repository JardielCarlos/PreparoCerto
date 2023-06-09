from flask_restful import Resource, reqparse, marshal
from helpers.database import db
from helpers.logger import logger
from model.mensagem import Message, msgError

from model.unidade_medida import UnidadeMedida, unidadeFields

parser = reqparse.RequestParser()

parser.add_argument("sigla", type=str, help="sigla nao informada", required=True)

class Unidade(Resource):
    
    def get(self):
      # logger.info("Proprietarios listados com Sucesso")

      return marshal(UnidadeMedida.query.all(), unidadeFields), 200
    
    def post(self):
      args = parser.parse_args()

      try:
        unidade = UnidadeMedida(args['sigla'])

        db.session.add(unidade)
        db.session.commit()

        logger.info(f"unidade de id: {unidade.id} criado com sucesso")
        return marshal(unidade, unidadeFields), 201
      except:
        logger.error("Error ao cadastrar o unidade")

        codigo = Message(2, "Error ao cadastrar o unidade")
        return marshal(codigo, msgError), 400

