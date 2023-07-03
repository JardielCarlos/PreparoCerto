from flask_restful import Resource, marshal, reqparse
from helpers.database import db
from helpers.logger import logger
from helpers.auth.token_verifier import token_verify

from model.mensagem import Message, msgFields
from model.preparacao_ingrediente import PreparacaoIngrediente, preparacaoIngredienteToken, ingredientesTokenFields
from model.ingrediente import Ingrediente
from model.preparacao import Preparacao
from model.unidade_medida import UnidadeMedida
from model.medida_caseira import MedidaCaseira

parser = reqparse.RequestParser()

parser.add_argument("preparacao", type=dict, help="Preparação não informada", required=True)
parser.add_argument("ingrediente", type=dict, help="Ingrediente não informado", required=True)
parser.add_argument("pesoBruto", type=float, help="Peso Bruto não informado", required=False)
parser.add_argument("unidade", type=dict, help="Unidade não informada", required=False)
parser.add_argument("indicadorParteComestivel", type=float, help="Indicador de Parte Comestível não informado", required=False)
parser.add_argument("pesoLiquido", type=float, help="Peso Liquido não informado", required=False)
parser.add_argument("perCapita", type=float, help="Per Capita não informada", required=False)
parser.add_argument("medidaCaseira", type=dict, help="Medida Caseira não informada", required=False)
parser.add_argument("embalagem", type=float, help="Embalagem não informada", required=False)
parser.add_argument("preco", type=float, help="Preço não informado", required=False)
parser.add_argument("custoPreparacao", type=float, help="Custo na preparação não informado", required=False)


class PreparacaoIngredientes(Resource):
  @token_verify
  def get(self, tipo, refreshToken):
    if tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar os ingredientes da preparacao")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

    preparacaoIngrediente = PreparacaoIngrediente.query.all()

    data = {'preparacaoIngrediente':preparacaoIngrediente, 'token': refreshToken}

    logger.info("Preparação-Ingrediente listados com sucesso")
    return marshal(data, preparacaoIngredienteToken), 200

  @token_verify
  def post(self, tipo, refreshToken):
    if tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar os ingredientes da preparacao")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

    args = parser.parse_args()
    try:
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
        codigo = Message(1, f"Medida Caseira de id: {medidaCaseiraId} não encontrada")
        return marshal(codigo, msgFields), 404
      elif pesoBruto is None:
        codigo = Message(1, f"Peso bruto não informado")
        return marshal(codigo, msgFields), 404
      elif indicadorParteComestivel is None:
        codigo = Message(1, f"indicador de Parte Comestivel não informado")
        return marshal(codigo, msgFields), 404
      elif pesoLiquido is None:
        codigo = Message(1, f"Peso liquido não informado")
        return marshal(codigo, msgFields), 404
      elif perCapita is None:
        codigo = Message(1, f"Per capita não informada")
        return marshal(codigo, msgFields), 404
      elif embalagem is None:
        codigo = Message(1, f"Embalagem não informado")
        return marshal(codigo, msgFields), 404
      elif preco is None:
        codigo = Message(1, f"preço não informado")
        return marshal(codigo, msgFields), 404
      elif custoPreparacao is None:
        codigo = Message(1, f"custo da preparacao não informado")
        return marshal(codigo, msgFields), 404

      preparacaoIngrediente = PreparacaoIngrediente(preparacao, ingrediente, pesoBruto, unidade, indicadorParteComestivel, pesoLiquido, perCapita, medidaCaseira, embalagem, preco, custoPreparacao)

      db.session.add(preparacaoIngrediente)
      db.session.commit()

      data = {'preparacaoIngrediente': preparacaoIngrediente, 'token': refreshToken}

      logger.info(f"Preparação-Ingrediente de id: {preparacaoIngrediente.id} criado com sucesso")
      return marshal(data, preparacaoIngredienteToken), 201
    except:
      logger.error("Erro ao cadastrar a Preparacao-Ingrediente")

      codigo = Message(1, '"Erro ao cadastrar a Preparacao-Ingrediente"')
      return marshal(codigo, msgFields), 400


class PreparacaoIngredientesId(Resource):
  @token_verify
  def get(self, tipo, refreshToken, id):
    if tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar os ingredientes da preparacao")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

    preparacao = Preparacao.query.get(id)
    ingredientes = PreparacaoIngrediente.query.filter_by(preparacao_id=id).all()

    if preparacao is None:
      logger.error(f"Preparação de id: {id} não encontrada")

      codigo = Message(1, f"Preparação de id: {id} não encontrada")
      return marshal(codigo, msgFields), 404
    print(ingredientes[0].ingrediente.nome)
    data = {'ingredientes': ingredientes, 'token': refreshToken}

    return marshal(data, ingredientesTokenFields), 200

  @token_verify
  def put(self, tipo, refreshToken, id):
    if tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar os ingredientes da preparacao")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

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

      data = {'preparacaoIngrediente': preparacaoIngredienteBd, 'token': refreshToken}


      logger.info(f"Preparação-Ingrediente de id: {id} atualizada com sucesso")
      return marshal(data, preparacaoIngredienteToken), 200
    except:
      logger.error("Erro ao atualizar o Preparação-Ingrediente")

      codigo = Message(2, "Erro ao atualizar o Preparação-Ingrediente")
      return marshal(codigo, msgFields), 400

  @token_verify
  def delete(self, tipo, refreshToken, id):
    if tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar os ingredientes da preparacao")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403
    preparacaoIngredienteBd = PreparacaoIngrediente.query.get(id)

    if preparacaoIngredienteBd is None:
      logger.error(f"Preparação-Ingrediente de id: {id} não encontrada")

      codigo = Message(1, f"Preparação-Ingrediente de id: {id} não encontrada")
      return marshal(codigo, msgFields), 404

    db.session.delete(preparacaoIngredienteBd)
    db.session.commit()

    logger.info(f"Preparação-Ingrediente de id: {id} deletada com sucesso")
    return {'token': refreshToken}, 200
