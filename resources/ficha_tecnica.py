from flask_restful import Resource, marshal
                                                 
from model.ficha_tecnica import fichaTecnicaOperacionalFields, fichaTecnicaGerencialFields, fichaTecnicaGerencialTotalFields
from model.preparacao_ingrediente import PreparacaoIngrediente


class FichaTecnicaOperacional(Resource):
    def get(self, id):
        preparacaoIngrediente = PreparacaoIngrediente.query.filter_by(preparacao_id=id).all()
        return marshal(preparacaoIngrediente, fichaTecnicaOperacionalFields), 200


class FichaTecnicaGerencial(Resource):
    def get(self, id):
        preparacaoIngrediente = PreparacaoIngrediente.query.filter_by(preparacao_id=id).all()
        total = 0
        data = {"preparacao_ingrediente": preparacaoIngrediente, "total": total}

        return marshal(data, fichaTecnicaGerencialTotalFields), 200
