from flask_restful import Resource, marshal

from model.ficha_tecnica import fichaTecnicaGerencialFields, fichaTecnicaOperacionalFields
from model.preparacao_ingrediente import PreparacaoIngrediente
from model.modo_preparo import ModoPreparo
from model.utensilio_preparacao import UtensilioPreparacao
from model.mensagem import Message, msgFields

class FichaTecnicaOperacional(Resource):
  def get(self, id):
    preparacaoIngrediente = PreparacaoIngrediente.query.filter_by(preparacao_id=id).all()

    modoPreparo = ModoPreparo.query.filter_by(preparacao_id=id).all()
    preparacaoUtensilio = UtensilioPreparacao.query.filter_by(preparacao_id=id).all()

    if modoPreparo is None:
      codigo = Message(1, "A preparação não possui um modo de preparo")
      return marshal(codigo, msgFields)

    elif preparacaoUtensilio == []:
      codigo = Message(1, "A preparação não possui utensilios")
      return marshal(codigo, msgFields), 404

    data = {
      "preparacao_ingrediente": preparacaoIngrediente,
      "modoPreparo": modoPreparo,
      "preparacao_utensilio": preparacaoUtensilio
    }

    return marshal(data, fichaTecnicaOperacionalFields), 200


class FichaTecnicaGerencial(Resource):
  def get(self, id):
    preparacaoIngrediente = PreparacaoIngrediente.query.filter_by(preparacao_id=id).all()


    if preparacaoIngrediente is None:
      codigo = Message(1, "A preparação não possui ingredientes")
      return marshal(codigo, msgFields)



    valorSugerido = None
    total = 0
    for prepIngred in preparacaoIngrediente:
      total += prepIngred.preco

    data = {
      "preparacao_ingrediente": preparacaoIngrediente,
      "total": total,
      "valor_sugerido": valorSugerido
    }

    return marshal(data, fichaTecnicaGerencialFields), 200
