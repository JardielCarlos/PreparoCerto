from flask_restful import Resource, marshal, reqparse
from helpers.database import db
from helpers.logger import logger
from model.mensagem import Message, msgError

from model.ficha_tecnica import fichaTecnicaOperacionalFields, fichaTecnicaGerencialFields
from model.ingrediente_preparacao import IngredientePreparacao, ingredientePreparacaoFields

class jFichaTecnicaOperacional(Resource):
    def get(self, id):
        IngredientePreparacaoBd = IngredientePreparacao.query.all()
        lista = []
        for i in range(len(IngredientePreparacaoBd)):
            fichaTecnica = IngredientePreparacaoBd[i]
            if fichaTecnica.preparacao_id == id:
                lista.append(fichaTecnica)

        return marshal(lista, fichaTecnicaOperacionalFields), 200
    
class FichaTecnicaGerencial(Resource):
    def get(self, id):
        IngredientePreparacaoBd = IngredientePreparacao.query.all()
        lista = []
        for i in range(len(IngredientePreparacaoBd)):
            fichaTecnica = IngredientePreparacaoBd[i]
            if fichaTecnica.preparacao_id == id:
                lista.append(fichaTecnica)

        return marshal(lista, fichaTecnicaGerencialFields), 200
    