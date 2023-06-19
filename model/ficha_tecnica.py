from flask_restful import fields
from model.unidade_medida import unidadeFields
from model.medida_caseira import medidaCaseiraFields
from model.ingrediente import ingredienteFields
from model.preparacao import preparacaoFields

fichaTecnicaOperacionalFields = {
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

fichaTecnicaGerencialFields = {
    'id': fields.Integer,
    'ingrediente': fields.Nested(ingredienteFields),
    'preparacao': fields.Nested(preparacaoFields),
    'embalagem': fields.Float,
    'preco': fields.Float,
    'custoPreparacao': fields.Float
}

fichaTecnicaGerencialTotalFields = {
    'preparacao_ingrediente': fields.Nested(fichaTecnicaGerencialFields),
    'total': fields.Float
}