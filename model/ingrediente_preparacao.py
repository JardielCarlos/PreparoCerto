from flask_restful import fields
from helpers.database import db
from model.ingrediente import ingredienteFields
from model.preparacao import preparacaoFields
from model.unidade_medida import unidadeFields
from model.medida_caseira import medidaCaseiraFields

ingredientePreparacaoFields = {'id': fields.Integer, 'ingrediente': fields.Nested(ingredienteFields), 'preparacao': fields.Nested(preparacaoFields), 'pesoBruto': fields.Float, 'indicadorParteComestivel': fields.Float, 'pesoLiquido': fields.Float, 'perCapita': fields.Float, 'embalagem': fields.Float, 'preco': fields.Float, 'custPreparacao': fields.Float,'unPesoBruto': fields.Nested(unidadeFields),'unPesoLiquido': fields.Nested(unidadeFields),'unPerCapita': fields.Nested(unidadeFields),'medidaCaseira':fields.Nested(medidaCaseiraFields)}

class IngredientePreparacao(db.Model):
    __tablename__ = "tb_ingredientepreparacao"

    id = db.Column(db.Integer, primary_key=True)
    ingrediente_id = db.Column(db.Integer, db.ForeignKey("tb_ingrediente.id"))
    preparacao_id = db.Column(db.Integer, db.ForeignKey("tb_preparacao.id"))
    pesoBruto = db.Column(db.Float, nullable=False)
    unidade = db.Column(db.String, nullable=False)
    indicadorParteComestivel = db.Column(db.Float, nullable=False)
    pesoLiquido = db.Column(db.Float,nullable=False)
    perCapita = db.Column(db.Float, nullable=False)
    embalagem = db.Column(db.Float, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    custPreparacao = db.Column(db.Float, nullable=False)
    unPesoBruto_id = db.Column(db.Integer, db.ForeignKey("tb_unidademedida.id"))
    unPesoLiquido_id = db.Column(db.Integer, db.ForeignKey("tb_unidademedida.id"))
    unPerCapita_id = db.Column(db.Integer, db.ForeignKey("tb_unidademedida.id"))

    ingrediente = db.relationship("Ingrediente", uselist=False)
    preparacao = db.relationship("Preparacao", uselist=False)
    unPesoBruto = db.relationship("UnidadeMedida",uselist=False)
    unPesoLiquido = db.relationship("UnidadeMedida",uselist=False)
    unPerCapita= db.relationship("UnidadeMedida",uselist=False)

    def __init__(self, ingrediente, preparacao, pesoBruto, unidade, indicadorParteComestivel, pesoLiquido, perCapita, embalagem, preco, custPreparacao):
        self.ingrediente = ingrediente
        self.preparacao = preparacao
        self.pesoBruto = pesoBruto
        self.unidade = unidade
        self.indicadorParteComestivel = indicadorParteComestivel
        self.pesoLiquido = pesoLiquido
        self.perCapita = perCapita
        self.embalagem = embalagem
        self.preco = preco
        self.custPreparacao = custPreparacao

    def __repr__(self):
      return f'<IngredientePreparacao {self.id}>'