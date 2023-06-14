from flask_restful import Resource, marshal

from model.ficha_tecnica import fichaTecnicaOperacionalFields, fichaTecnicaGerencialFields
from model.preparacao_ingrediente import PreparacaoIngrediente


class FichaTecnicaOperacional(Resource):
    def get(self, id):
        IngredientePreparacaoBd = PreparacaoIngrediente.query.all()
        lista = []
        for i in range(len(IngredientePreparacaoBd)):
            fichaTecnica = IngredientePreparacaoBd[i]
            if fichaTecnica.preparacao_id == id:
                lista.append(fichaTecnica)

        return marshal(lista, fichaTecnicaOperacionalFields), 200


class FichaTecnicaGerencial(Resource):
    def get(self, id):
        IngredientePreparacaoBd = PreparacaoIngrediente.query.all()
        lista = []
        total = 0
        for i in range(len(IngredientePreparacaoBd)):
            fichaTecnica = IngredientePreparacaoBd[i]
            if fichaTecnica.preparacao_id == id:
                total += fichaTecnica.preco
                lista.append(fichaTecnica)
        print(total)

        return marshal(lista, fichaTecnicaGerencialFields), 200