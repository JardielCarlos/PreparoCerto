from flask_restful import fields
from helpers.database import db
from model.ingrediente import ingredienteFields
from model.preparacao import preparacaoFields

ingredientePreparacaoFields = {'id': fields.Integer, 'ingrediente': fields.Nested(ingredienteFields), 'preparacao': fields.Nested(preparacaoFields)}

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

    unPesoBruto = db.relationship("UnidadeMedida",uselist=False)
    unPesoLiquido = db.relationship("UnidadeMedida",uselist=False)
    unPerCapita= db.relationship("UnidadeMedida",uselist=False)

    def __init__(self, ingrediente, preparacao, pesoBruto, unidade, indicadorParteComestivel, pesoLiquido, perCapita, embalagem, preco, custPreparacao):
        self.ingrediente = ingrediente
        self.preparacao = preparacao

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
        self.embalagem = embalagem
        self.preco = preco
        self.custPreparacao = custPreparacao
        self.medidaCaseira = medidaCaseira
        self.embalagem = embalagem
        self.preco = preco
        self.custoPreparacao = custoPreparacao
        

    def __repr__(self):
      return f'<IngredientePreparacao {self.id}>'