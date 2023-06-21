from flask_restful import fields
from model.unidade_medida import unidadeFields
from model.medida_caseira import medidaCaseiraFields
from model.ingrediente import ingredienteFields
from model.preparacao import preparacaoFields
from model.utensilio_preparacao import utensilioPreparacaoFields
from model.modo_preparo import modoPreparoFields

ingredienteOperacionalFields = {
    'id': fields.Integer,
    'ingrediente': fields.Nested(ingredienteFields),
    'preparacao': fields.Nested(preparacaoFields),
    'pesoBruto': fields.Float,
    'unidade': fields.Nested(unidadeFields),
    'indicadorParteComestivel': fields.Float,
    'pesoLiquido': fields.Float,
    'perCapita': fields.Float,
    'medidaCaseira': fields.Nested(medidaCaseiraFields)
    }

ingredienteGerencialFields = {
    'id': fields.Integer,
    'ingrediente': fields.Nested(ingredienteFields),
    'preparacao': fields.Nested(preparacaoFields),
    'embalagem': fields.Float,
    'preco': fields.Float,
    'custoPreparacao': fields.Float
}

fichaTecnicaOperacionalFields = {
    'ingredientes': fields.Nested(ingredienteOperacionalFields),
    'modoPreparo': fields.Nested(modoPreparoFields),
    'utensilios': fields.Nested(utensilioPreparacaoFields)
}

fichaTecnicaGerencialFields = {
    'ingredientes': fields.Nested(ingredienteGerencialFields),
    'numPorcoes': fields.Float,
    'total': fields.Float,
    'valorPorcao': fields.Float,
    'valorSugerido': fields.Float
}
