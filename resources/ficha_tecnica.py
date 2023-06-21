from flask_restful import Resource, marshal, reqparse

from model.ficha_tecnica import fichaTecnicaGerencialFields, fichaTecnicaOperacionalFields
from model.preparacao_ingrediente import PreparacaoIngrediente
from model.preparacao import Preparacao
from model.modo_preparo import ModoPreparo
from model.utensilio_preparacao import UtensilioPreparacao
from model.mensagem import Message, msgFields

from helpers.functions.calcularValorSugerido import calcularValorSugerido

from sqlalchemy.sql.functions import sum
from helpers.functions.calcularValorSugerido import calcularValorSugerido

parser = reqparse.RequestParser()

parser.add_argument("perImposto", type=float, help="Percentual de imposto não informado", required=True)
parser.add_argument("perLucro", type=float, help="Percentual de lucro não informado", required=True)


class FichaTecnicaOperacional(Resource):
  def get(self, id):
    preparacaoIngrediente = PreparacaoIngrediente.query.filter_by(preparacao_id=id).all()
    modoPreparo = ModoPreparo.query.filter_by(preparacao_id=id).all()
    preparacaoUtensilio = UtensilioPreparacao.query.filter_by(preparacao_id=id).all()

    preparacao = Preparacao.query.get(id)

    if preparacaoIngrediente == []:
      codigo = Message(1, "A preparação não possui nenhum ingrediente cadastrado")
      return marshal(codigo, msgFields), 404

    elif modoPreparo == []:
      codigo = Message(1, "A preparação não possui um modo de preparo")
      return marshal(codigo, msgFields), 404

    elif preparacaoUtensilio == []:
      codigo = Message(1, "A preparação não possui utensilios")
      return marshal(codigo, msgFields), 404

    elif preparacao is None:
      codigo = Message(1, f"Preparação de id: {id} não encontrada")
      return marshal(codigo, msgFields), 404

    data = {
      "ingredientes": preparacaoIngrediente,
      "modoPreparo": modoPreparo,
      "utensilios": preparacaoUtensilio,
      "numPorcoes": preparacao.numPorcoes
    }

    return marshal(data, fichaTecnicaOperacionalFields), 200

class FichaTecnicaGerencial(Resource):
  def get(self, id):
    args = parser.parse_args()

    preparacaoIngrediente = PreparacaoIngrediente.query.filter_by(preparacao_id=id).all()
    preparacao = Preparacao.query.get(id)

    if preparacaoIngrediente == []:
      codigo = Message(1, "A preparação não possui nenhum ingrediente cadastrado")
      return marshal(codigo, msgFields), 404

    elif preparacao is None:
      codigo = Message(1, f"Preparação de id: {id} não encontrada")
      return marshal(codigo, msgFields), 404

    total = 0
    for prepIngred in preparacaoIngrediente:
      total += prepIngred.preco

    valorPorcao = total / preparacao.numPorcoes

    valorSugerido = calcularValorSugerido(valorPorcao, args['perImposto'], args['perLucro'])

    data = {
      "ingredientes": preparacaoIngrediente,
      "numPorcoes": preparacao.numPorcoes,
      "total": total,
      "valorPorcao": valorPorcao,
      "valorSugerido": valorSugerido
    }

    return marshal(data, fichaTecnicaGerencialFields), 200
