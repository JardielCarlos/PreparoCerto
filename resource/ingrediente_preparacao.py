from flask_restful import Resource, marshal, reqparse
from helpers.database import db
from helpers.logger import logger
from model.mensagem import Message, msgError

from model.ingrediente_preparacao import IngredientePreparacao, ingredientePreparacaoFields
from model.ingrediente import Ingrediente
from model.preparacao import Preparacao

parser = reqparse.RequestParser()

parser.add_argument("ingrediente", type=dict, help="ingrediente nao informado", required=True)
parser.add_argument("preparacao", type=dict, help="preparacao nao informado", required=True)

class IngredientesPreparacao(Resource):
  def get(self):
    logger.info("Ingredientes-Preparacao listados com sucesso")
    return marshal(IngredientePreparacao.query.all(), ingredientePreparacaoFields), 200
  
  def post(self):
    args = parser.parse_args()

    ingredienteId = args['ingrediente']['id']
    preparacaoId = args['preparacao']['id']

    ingrediente = Ingrediente.query.get(ingredienteId)
    preparacao = Preparacao.query.get(preparacaoId)
    if ingrediente is None:
      codigo = Message(1, f"Ingrediente de id: {ingredienteId} não encontrado")
      return marshal(codigo, msgError), 404
    elif preparacao is None:
      codigo = Message(1, f"Preparacao de id: {ingredienteId} não encontrada")
      return marshal(codigo, msgError), 404
    
    ingredientePreparacao = IngredientePreparacao(ingrediente, preparacao)
    db.session.add(ingredientePreparacao)
    db.session.commit()

    logger.info(f"IngredientePreparação de id: {ingredientePreparacao.id} criado com sucesso")
    return marshal(ingredientePreparacao, ingredientePreparacaoFields), 201
  
class IngredientesPreparacaoId(Resource):
  def get(self, id):
    logger.info("Ingrediente-Preparacao listados com sucesso")
    return marshal(IngredientePreparacao.query.get(id), ingredientePreparacaoFields), 200

  def put(self, id):
    args = parser.parse_args()

    ingredientePreparacaoBd = IngredientePreparacao.query.get(id)
    ingredienteId = args['ingrediente']['id']
    preparacaoId = args['preparacao']['id']

    ingrediente = Ingrediente.query.get(ingredienteId)
    preparacao = Preparacao.query.get(preparacaoId)
    if ingrediente is None:
      codigo = Message(1, f"Ingrediente de id: {ingredienteId} não encontrado")
      return marshal(codigo, msgError), 404
    elif preparacao is None:
      codigo = Message(1, f"Preparacao de id: {ingredienteId} não encontrada")
      return marshal(codigo, msgError), 404

    ingredientePreparacaoBd.ingrediente = ingrediente
    ingredientePreparacaoBd.preparacao = preparacao

    db.session.add(ingredientePreparacaoBd)
    db.session.commit()

    logger.info(f"ingredientePreparacao de id: {id} atualizada com sucesso")
    return marshal(ingredientePreparacaoBd, ingredientePreparacaoFields)
  
  def delete(self, id):
    ingredientePreparacaoBd = IngredientePreparacao.query.get(id)

    if ingredientePreparacaoBd is None:
      logger.error(f"ingredientePreparacao de id: {id} nao encontrado")

      codigo = Message(1, f"ingredientePreparacao de id: {id} nao encontrado")
      return marshal(codigo, msgError), 404
    
    db.session.delete(ingredientePreparacaoBd)
    db.session.commit()

    logger.info(f"Ingrediente de id: {id} deletado com sucesso")
    return {}, 200
