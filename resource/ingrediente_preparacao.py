from flask_restful import Resource, marshal, reqparse
from helpers.database import db
from helpers.logger import logger
from model.mensagem import Message, msgError

from model.ingrediente_preparacao import IngredientePreparacao, ingredientePreparacaoFields
from model.ingrediente import Ingrediente
from model.preparacao import Preparacao
from model.unidade_medida import UnidadeMedida
from model.medida_caseira import MedidaCaseira

parser = reqparse.RequestParser()

parser.add_argument("preparacao", type=dict, help="preparacao nao informado", required=True)
parser.add_argument("ingrediente", type=dict, help="ingrediente nao informado", required=True)
parser.add_argument("pesoBruto", type=float, help="pesoBruto nao informado", required=True)
parser.add_argument("unidade", type=dict, help="unidade nao informado", required=True)
parser.add_argument("indicadorParteComestivel", help="indicadorParteComestivel nao informado", type=float, required=True)
parser.add_argument("pesoLiquido", type=float, help="pesoLiquido nao informado", required=True)
parser.add_argument("perCapita", type=float, help="perCapita nao informado", required=True)
parser.add_argument("medidaCaseira", type=dict, help="medidaCaseira nao informado", required=True)
parser.add_argument("embalagem", type=float, help="embalagem nao informado", required=True)
parser.add_argument("preco", type=float, help="preco nao informado", required=True)
parser.add_argument("custoPreparacao",type=float, help="custoPreparacao nao informado", required=True)

class IngredientesPreparacao(Resource):
  def get(self):
    logger.info("Ingredientes-Preparacao listados com sucesso")
    return marshal(IngredientePreparacao.query.all(), ingredientePreparacaoFields), 200
  
  def post(self):
    args = parser.parse_args()

    preparacaoId = args['preparacao']['id']
    ingredienteId = args['ingrediente']['id']

    pesoBruto = args['pesoBruto']
    
    unidadeId = args['unidade']['id']
    
    indicadorParteComestivel = args['indicadorParteComestivel']
    pesoLiquido = args['pesoLiquido']
    perCapita = args['perCapita']
    medidaCaseiraId = args['medidaCaseira']['id']
    embalagem = args['embalagem']
    preco = args['preco']
    custoPreparacao = args['custoPreparacao']



    ingrediente = Ingrediente.query.get(ingredienteId)
    preparacao = Preparacao.query.get(preparacaoId)
    unidade = UnidadeMedida.query.get(unidadeId)
    medidaCaseira = MedidaCaseira.query.get(medidaCaseiraId)
    if ingrediente is None:
      codigo = Message(1, f"Ingrediente de id: {ingredienteId} não encontrado")
      return marshal(codigo, msgError), 404
    elif preparacao is None:
      codigo = Message(1, f"Preparacao de id: {preparacaoId} não encontrada")
      return marshal(codigo, msgError), 404
    
    ingredientePreparacao = IngredientePreparacao(preparacao, ingrediente, pesoBruto, unidade, indicadorParteComestivel, pesoLiquido, perCapita, medidaCaseira, embalagem, preco, custoPreparacao)
    db.session.add(ingredientePreparacao)
    db.session.commit()

    logger.info(f"IngredientePreparação de id: {ingredientePreparacao.id} criado com sucesso")
    return marshal(ingredientePreparacao, ingredientePreparacaoFields), 201
  
class IngredientesPreparacaoId(Resource):
  def get(self, id):

    ingredientePreparacao = IngredientePreparacao.query.get(id)
    if ingredientePreparacao is None:
      codigo = Message(1, f"IngredientePreparacao de id: {id} não encontrado")
      return marshal(codigo, msgError), 404
    logger.info("Ingrediente-Preparacao listados com sucesso")
    return marshal(IngredientePreparacao.query.get(id), ingredientePreparacaoFields), 200

  def put(self, id):
    args = parser.parse_args()
    try:

      ingredientePreparacaoBd = IngredientePreparacao.query.get(id)
      ingredienteId = args['ingrediente']['id']
      preparacaoId = args['preparacao']['id']

      if ingredientePreparacaoBd is None:
        logger.error(f"IngredientePreparacao de id: {id} nao encontrada")

        codigo = Message(1, f"IngredientePreparacao de id: {id} nao encontrada")
        return marshal(codigo, msgError), 404

      ingrediente = Ingrediente.query.get(ingredienteId)
      preparacao = Preparacao.query.get(preparacaoId)
      if ingrediente is None:
        codigo = Message(1, f"Ingrediente de id: {ingredienteId} não encontrado")
        return marshal(codigo, msgError), 404
      elif preparacao is None:
        codigo = Message(1, f"Preparacao de id: {preparacaoId} não encontrada")
        return marshal(codigo, msgError), 404

      ingredientePreparacaoBd.ingrediente = ingrediente
      ingredientePreparacaoBd.preparacao = preparacao

      db.session.add(ingredientePreparacaoBd)
      db.session.commit()

      logger.info(f"ingredientePreparacao de id: {id} atualizada com sucesso")
      return marshal(ingredientePreparacaoBd, ingredientePreparacaoFields)
    except:
      logger.error("Erro ao atualizar o IngredientePreaparacao")

      codigo = Message(2, "Erro ao atualizar o IngredientePreaparacao")
      return marshal(codigo, msgError), 400
  
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
