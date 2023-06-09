from flask_restful import fields
from helpers.database import db
from model.ingrediente import ingredienteFields
from model.preparacao import preparacaoFields
from model.unidade_medida import unidadeFields
from model.medida_caseira import medidaCaseiraFields

ingredientePreparacaoFields = {
    'id': fields.Integer,
    'preparacao': fields.Nested(preparacaoFields),
    'ingrediente': fields.Nested(ingredienteFields),
    'pesoBruto': fields.Float,
    'unidade': fields.Nested(unidadeFields),
    'indicadorParteComestivel': fields.Float,
    'pesoLiquido': fields.Float,
    'medidaCaseira': fields.Nested(medidaCaseiraFields),
    'embalagem': fields.Float,
    'preco': fields.Float,
    'custoPreparacao': fields.Float
    }

class IngredientePreparacao(db.Model):
    __tablename__ = "tb_ingredientepreparacao"

    id = db.Column(db.Integer, primary_key=True)
    preparacao_id = db.Column(db.Integer, db.ForeignKey("tb_preparacao.id"))
    ingrediente_id = db.Column(db.Integer, db.ForeignKey("tb_ingrediente.id"))

    pesoBruto = db.Column(db.Float, nullable=False)
    unidade_id = db.Column(db.Integer, db.ForeignKey("tb_unidademedida.id"))
    indicadorParteComestivel = db.Column(db.Float, nullable=False)
    pesoLiquido = db.Column(db.Float, nullable=False)
    perCapita = db.Column(db.Float, nullable=False)
    medidaCaseira_id = db.Column(db.Integer, db.ForeignKey("tb_medidacaseira.id"))
    embalagem = db.Column(db.Float, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    custoPreparacao = db.Column(db.Float, nullable=False)

    preparacao = db.relationship("Preparacao", uselist=False)
    ingrediente = db.relationship("Ingrediente", uselist=False)
    unidade = db.relationship("UnidadeMedida", uselist=False)
    medidaCaseira = db.relationship("MedidaCaseira", uselist=False)
    

    def __init__(self, preparacao, ingrediente, pesoBruto, unidade, indicadorParteComestivel, pesoLiquido, perCapita, medidaCaseira, embalagem, preco, custoPreparacao):
        self.preparacao = preparacao
        self.ingrediente = ingrediente
        self.pesoBruto = pesoBruto
        self.unidade = unidade
        self.indicadorParteComestivel = indicadorParteComestivel
        self.pesoLiquido = pesoLiquido
        self.perCapita = perCapita
        self.medidaCaseira = medidaCaseira
        self.embalagem = embalagem
        self.preco = preco
        self.custoPreparacao = custoPreparacao
        

    def __repr__(self):
      return f'<IngredientePreparacao {self.id}>'