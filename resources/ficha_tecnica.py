from flask_restful import Resource, marshal

from model.ficha_tecnica import fichaTecnicaOperacionalFields, fichaTecnicaGerencialTotalFields
from model.preparacao_ingrediente import PreparacaoIngrediente
from model.modo_preparo import ModoPreparo
from model.utensilio_preparacao import UtensilioPreparacao
from model.mensagem import Message, msgFields
from sqlalchemy.sql.functions import sum
from helpers.functions.calcularValorSugerido import calcularValorSugerido

class FichaTecnicaOperacional(Resource):
  def get(self, id):
    preparacaoIngrediente = PreparacaoIngrediente.query.filter_by(preparacao_id=id).all()
    return marshal(preparacaoIngrediente, fichaTecnicaOperacionalFields), 200


class FichaTecnicaGerencial(Resource):
  def get(self, id, perImposto, perLucro):
    preparacaoIngrediente = PreparacaoIngrediente.query.filter_by(preparacao_id=id).all()
    modoPreparo = ModoPreparo.query.filter_by(preparacao_id=id).all()
    preparacaoUtensilio = UtensilioPreparacao.query.filter_by(preparacao_id=id).all()
    print(preparacaoUtensilio)

    if preparacaoIngrediente is None:
      codigo = Message(1, "A preparação não possui ingredientes")
      return marshal(codigo, msgFields)

    elif modoPreparo is None:
      codigo = Message(1, "A preparação não possui um modo de preparo")
      return marshal(codigo, msgFields)

    elif preparacaoUtensilio == []:
      codigo = Message(1, "A preparação não possui utensilios")
      return marshal(codigo, msgFields), 404

    total = 0
    for prepIngred in preparacaoIngrediente:
      total += prepIngred.preco
    valorSugerido = calcularValorSugerido(total,perImposto,perLucro)

    data = {
      "preparacao_ingrediente": preparacaoIngrediente,
      "preparacao_utensilio": preparacaoUtensilio,
      "modoPreparo": modoPreparo,
      "total": total,
      "valorSugerido": valorSugerido
    }

    return marshal(data, fichaTecnicaGerencialTotalFields), 200
