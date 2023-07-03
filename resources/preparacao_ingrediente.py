from flask_restful import Resource, marshal, reqparse
from helpers.database import db
from helpers.logger import logger
from model.mensagem import Message, msgFields

from model.preparacao_ingrediente import PreparacaoIngrediente, preparacaoIngredienteFields, ingredientesFields
from model.ingrediente import Ingrediente
from model.preparacao import Preparacao
from model.unidade_medida import UnidadeMedida
from model.medida_caseira import MedidaCaseira

parser = reqparse.RequestParser()

parser.add_argument("preparacao", type=dict, help="Preparação não informada", required=True)
parser.add_argument("ingrediente", type=dict, help="Ingrediente não informado", required=True)
parser.add_argument("pesoBruto", type=float, help="Peso Bruto não informado", required=True)
parser.add_argument("unidade", type=dict, help="Unidade não informada", required=True)
parser.add_argument("indicadorParteComestivel", type=float, help="Indicador de Parte Comestível não informado", required=True)
parser.add_argument("pesoLiquido", type=float, help="Peso Liquido não informado", required=True)
parser.add_argument("perCapita", type=float, help="Per Capita não informada", required=True)
parser.add_argument("medidaCaseira", type=dict, help="Medida Caseira não informada", required=True)
parser.add_argument("embalagem", type=float, help="Embalagem não informada", required=True)
parser.add_argument("preco", type=float, help="Preço não informado", required=True)
parser.add_argument("custoPreparacao", type=float, help="Custo na preparação não informado", required=True)


class PreparacaoIngredientes(Resource):
  def get(self):
    logger.info("Preparação-Ingrediente listados com sucesso")
    return marshal(PreparacaoIngrediente.query.all(), preparacaoIngredienteFields), 200

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
      return marshal(codigo, msgFields), 404

    elif preparacao is None:
      codigo = Message(1, f"Preparação de id: {preparacaoId} não encontrada")
      return marshal(codigo, msgFields), 404

    elif unidade is None:
      codigo = Message(1, f"Unidade de id: {unidadeId} não encontrada")
      return marshal(codigo, msgFields), 404

    elif medidaCaseira is None:
      codigo = Message(1, f"Medida Caseira de id: {preparacaoId} não encontrada")
      return marshal(codigo, msgFields), 404

    preparacaoIngrediente = PreparacaoIngrediente(preparacao, ingrediente, pesoBruto, unidade, indicadorParteComestivel, pesoLiquido, perCapita, medidaCaseira, embalagem, preco, custoPreparacao)

    db.session.add(preparacaoIngrediente)
    db.session.commit()

    logger.info(f"Preparação-Ingrediente de id: {preparacaoIngrediente.id} criado com sucesso")
    return marshal(preparacaoIngrediente, preparacaoIngredienteFields), 201


class PreparacaoIngredientesId(Resource):
  def get(self, id):
    preparacao = Preparacao.query.get(id)
    ingredientes = PreparacaoIngrediente.query.filter_by(preparacao_id=id).all()
    print(ingredientes)

    if preparacao is None:
      logger.error(f"Preparação de id: {id} não encontrada")

      codigo = Message(1, f"Preparação de id: {id} não encontrada")
      return marshal(codigo, msgFields), 404

    return marshal(ingredientes, ingredientesFields), 200

  def put(self, id):
    args = parser.parse_args()
    try:
      preparacaoIngredienteBd = PreparacaoIngrediente.query.get(id)
      preparacaoId = args['preparacao']['id']
      ingredienteId = args['ingrediente']['id']

      if preparacaoIngredienteBd is None:
        logger.error(f"Preparação-Ingrediente de id: {id} não encontrada")

        codigo = Message(1, f"Preparação-Ingrediente de id: {id} não encontrada")
        return marshal(codigo, msgFields), 404

      ingrediente = Ingrediente.query.get(ingredienteId)
      preparacao = Preparacao.query.get(preparacaoId)
      if ingrediente is None:
        codigo = Message(1, f"Ingrediente de id: {ingredienteId} não encontrado")
        return marshal(codigo, msgFields), 404
      elif preparacao is None:
        codigo = Message(1, f"Preparação de id: {preparacaoId} não encontrada")
        return marshal(codigo, msgFields), 404

      preparacaoIngredienteBd.ingrediente = ingrediente
      preparacaoIngredienteBd.preparacao = preparacao

      db.session.add(preparacaoIngredienteBd)
      db.session.commit()

      logger.info(f"Preparação-Ingrediente de id: {id} atualizada com sucesso")
      return marshal(preparacaoIngredienteBd, preparacaoIngredienteFields)
    except:
      logger.error("Erro ao atualizar o Preparação-Ingrediente")

      codigo = Message(2, "Erro ao atualizar o Preparação-Ingrediente")
      return marshal(codigo, msgFields), 400

  def delete(self, id):
    preparacaoIngredienteBd = PreparacaoIngrediente.query.get(id)

    if preparacaoIngredienteBd is None:
      logger.error(f"Preparação-Ingrediente de id: {id} não encontrada")

      codigo = Message(1, f"Preparação-Ingrediente de id: {id} não encontrada")
      return marshal(codigo, msgFields), 404

    db.session.delete(preparacaoIngredienteBd)
    db.session.commit()

    logger.info(f"Preparação-Ingrediente de id: {id} deletada com sucesso")
    return {}, 200
