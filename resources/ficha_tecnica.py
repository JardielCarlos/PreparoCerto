from flask_restful import Resource, marshal, reqparse
from helpers.logger import logger

from model.ficha_tecnica import fichaTecnicaGerencialFields, fichaTecnicaGerencialTokenFields, fichaTecnicaOperacionalTokenFields
from model.preparacao_ingrediente import PreparacaoIngrediente
from model.preparacao import Preparacao
from model.modo_preparo import ModoPreparo
from model.preparacao_utensilio import PreparacaoUtensilio
from model.mensagem import Message, msgFields


from helpers.auth.token_verifier import token_verify

from helpers.functions.calcularValorSugerido import calcularValorSugerido

from helpers.functions.calcularValorSugerido import calcularValorSugerido

parser = reqparse.RequestParser()

parser.add_argument("perImposto", type=float, help="Percentual de imposto não informado", required=True)
parser.add_argument("perLucro", type=float, help="Percentual de lucro não informado", required=True)


class FichaTecnicaOperacional(Resource):
  @token_verify
  def get(self, tipo, refreshToken, id):
    if tipo != 'preparador' and tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar a ficha tecnica operacional")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

    preparacaoIngrediente = PreparacaoIngrediente.query.filter_by(preparacao_id=id).all()
    modoPreparo = ModoPreparo.query.filter_by(preparacao_id=id).all()
    preparacaoUtensilio = PreparacaoUtensilio.query.filter_by(preparacao_id=id).all()

    preparacao = Preparacao.query.get(id)

    if preparacao is None:
      codigo = Message(1, f"Preparação de id: {id} não encontrada")
      return marshal(codigo, msgFields), 404

    fichaTecnicaOperacional = {
      "ingredientes": preparacaoIngrediente,
      "modoPreparo": modoPreparo,
      "utensilios": preparacaoUtensilio,
      "numPorcoes": preparacao.numPorcoes
    }

    data = {"fichaTecnicaOperacional": fichaTecnicaOperacional, 'token': refreshToken}

    return marshal(data, fichaTecnicaOperacionalTokenFields), 200

class FichaTecnicaGerencial(Resource):
  @token_verify
  def get(self, tipo, refreshToken, id):
    if tipo != 'preparador' and tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar a ficha tecnica Gerencial")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

    args = parser.parse_args()

    preparacaoIngrediente = PreparacaoIngrediente.query.filter_by(preparacao_id=id).all()
    preparacao = Preparacao.query.get(id)

    if preparacao is None:
      codigo = Message(1, f"Preparação de id: {id} não encontrada")
      return marshal(codigo, msgFields), 404

    total = 0
    for prepIngred in preparacaoIngrediente:
      total += prepIngred.preco

    valorPorcao = total / preparacao.numPorcoes

    valorSugerido = calcularValorSugerido(valorPorcao, args['perImposto'], args['perLucro'])

    fichaTecnicaGerencial = {
      "ingredientes": preparacaoIngrediente,
      "numPorcoes": preparacao.numPorcoes,
      "total": total,
      "valorPorcao": valorPorcao,
      "valorSugerido": valorSugerido
    }

    data = {"fichaTecnicaGerencial": fichaTecnicaGerencial, "token": refreshToken}

    return marshal(data, fichaTecnicaGerencialTokenFields), 200
