from flask_restful import Resource, marshal

from model.ficha_tecnica import fichaTecnicaOperacionalFields, fichaTecnicaGerencialFields
from model.ficha_tecnica import fichaTecnicaOperacionalFields,fichaTecnicaGerencialFields
from model.preparacao_ingrediente import PreparacaoIngrediente
from model.fichatecnica_ingrediente_preparacao import FichaTecnicaIngredientePreparacao


class FichaTecnicaOperacional(Resource):
    def get(self, id):
        FichaTecnicaIngredientePreparacaoBd = db.session.query(
        FichaTecnica.id,
        Ingrediente.id.label('id_ingrediente'),
        Ingrediente.nome.label('nome_ingrediente'),
        Preparacao.id.label('id_preparacao'),
        Preparacao.nome.label('nome_preparacao'),
        FichaTecnicaIngredientePreparacao.fichatecnica_id,
        FichaTecnicaIngredientePreparacao.ingredientePreparacao_id,
        PreparacaoIngrediente.pesoBruto).select_from(FichaTecnicaIngredientePreparacao).join(FichaTecnica,FichaTecnica.id == FichaTecnicaIngredientePreparacao.fichatecnica_id).join(PreparacaoIngrediente, PreparacaoIngrediente.id == FichaTecnicaIngredientePreparacao.ingredientePreparacao_id).join(Preparacao,Preparacao.id == PreparacaoIngrediente.preparacao_id).join(Ingrediente,Ingrediente.id == PreparacaoIngrediente.ingrediente_id).filter(FichaTecnicaIngredientePreparacao.id == id)
        
        return marshal(FichaTecnicaIngredientePreparacaoBd, fichaTecnicaOperacionalFields), 200


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
