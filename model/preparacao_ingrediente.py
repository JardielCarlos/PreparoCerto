from flask_restful import fields
from helpers.database import db
from model.ingrediente import ingredienteFields
from model.preparacao import preparacaoFields
from model.unidade_medida import unidadeFields
from model.medida_caseira import medidaCaseiraFields

ingredientePreparacaoFields = {'id': fields.Integer, 'ingrediente': fields.Nested(ingredienteFields), 'preparacao': fields.Nested(preparacaoFields)}

ingredientePreparacaoFields = {
    'id': fields.Integer,
    'preparacao': fields.Nested(preparacaoFields),
    'ingrediente': fields.Nested(ingredienteFields),
    'pesoBruto': fields.Float,
    'indicadorParteComestivel': fields.Float,
    'pesoLiquido': fields.Float,
    'medidaCaseira': fields.Nested(medidaCaseiraFields),
    'embalagem': fields.Float,
    'preco': fields.Float,
    'custoPreparacao': fields.Float,
    'unPesoBruto': fields.Nested(unidadeFields),
    'unPesoLiquido': fields.Nested(unidadeFields),
    'unPerCapita': fields.Nested(unidadeFields)
    }


class PreparacaoIngrediente(db.Model):
    __tablename__ = "tb_preparacao_ingrediente"

    id = db.Column(db.Integer, primary_key=True)
    preparacao_id = db.Column(db.Integer, db.ForeignKey("tb_preparacao.id"))
    pesoBruto = db.Column(db.Float, nullable=False)
    indicadorParteComestivel = db.Column(db.Float, nullable=False)
    pesoLiquido = db.Column(db.Float,nullable=False)
    perCapita = db.Column(db.Float, nullable=False)
    embalagem = db.Column(db.Float, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    custPreparacao = db.Column(db.Float, nullable=False)
    unPesoBruto_id = db.Column(db.Integer, db.ForeignKey("tb_unidademedida.id"))
    unPesoLiquido_id = db.Column(db.Integer, db.ForeignKey("tb_unidademedida.id"))
    unPerCapita_id = db.Column(db.Integer, db.ForeignKey("tb_unidademedida.id"))
    ingrediente_id = db.Column(db.Integer, db.ForeignKey("tb_ingrediente.id"))

    pesoBruto = db.Column(db.Float, nullable=False)
    indicadorParteComestivel = db.Column(db.Float, nullable=False)
    pesoLiquido = db.Column(db.Float, nullable=False)
    perCapita = db.Column(db.Float, nullable=False)
    medidaCaseira_id = db.Column(db.Integer, db.ForeignKey("tb_medidacaseira.id"))
    embalagem = db.Column(db.Float, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    custoPreparacao = db.Column(db.Float, nullable=False)
    preparacao = db.relationship("Preparacao", uselist=False)

    unPesoBruto = db.relationship("UnidadeMedida", foreign_keys=[unPesoBruto_id])
    unPesoLiquido = db.relationship("UnidadeMedida", foreign_keys=[unPesoLiquido_id])
    unPerCapita = db.relationship("UnidadeMedida", foreign_keys=[unPerCapita_id])
    
    ingrediente = db.relationship("Ingrediente", uselist=False)
    medidaCaseira = db.relationship("MedidaCaseira", uselist=False)

    def __init__(self, preparacao, ingrediente, pesoBruto, indicadorParteComestivel, pesoLiquido, perCapita, medidaCaseira, embalagem, preco, custoPreparacao, unPesoBruto, unPesoLiquido, unPerCapita):
        self.preparacao = preparacao
        self.ingrediente = ingrediente
        self.pesoBruto = pesoBruto
        self.indicadorParteComestivel = indicadorParteComestivel
        self.pesoLiquido = pesoLiquido
        self.perCapita = perCapita
        self.embalagem = embalagem
        self.preco = preco
        self.custPreparacao = custPreparacao
        self.medidaCaseira = medidaCaseira
        self.embalagem = embalagem
        self.preco = preco
        self.custoPreparacao = custoPreparacao
        self.unPesoBruto = unPesoBruto
        self.unPesoLiquido = unPesoLiquido
        self.unPerCapita = unPerCapita

    def __repr__(self):
        return f'<IngredientePreparacao {self.id}>'
