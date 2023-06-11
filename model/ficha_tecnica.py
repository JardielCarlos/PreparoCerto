from flask_restful import fields

from helpers.database import db
from model.gestor import gestorFields
from model.preparacao import preparacaoFields
from model.unidade_medida import unidadeFields

fichaTecnicaFields = {'id': fields.Integer,'componente': fields.String,'tempoPreparo': fields.Integer,'numPorcao': fields.Float,'custoPreparo': fields.Float,'custoPorcao': fields.Float,'rendimento': fields.Float, 'pesoPorcao': fields.Float,'medidaPorcao': fields.String, 'indicadorConversao': fields.Float, 'fatorCorrecaoGlobal': fields.Float,'grauDificuldade': fields.String,'gestor': fields.Nested(gestorFields),'preparacao': fields.Nested(preparacaoFields),'unPesoPorcao':fields.Nested(unidadeFields)}

class FichaTecnica(db.Model):
    __tablename__ = "tb_fichatecnica"

    id = db.Column(db.Integer, primary_key=True)
    componente = db.Column(db.String, nullable=False)
    tempoPreparo = db.Column(db.Integer, nullable=False)
    numPorcao = db.Column(db.Float, nullable=False)
    custoPreparo = db.Column(db.Float, nullable=False)
    custoPorcao = db.Column(db.Float, nullable=False)
    rendimento = db.Column(db.Float, nullable=False)
    pesoPorcao = db.Column(db.Float, nullable=False)
    medidaPorcao = db.Column(db.String, nullable=False)
    indicadorConversao = db.Column(db.Float, nullable=False)
    fatorCorrecaoGlobal = db.Column(db.Float, nullable=False)
    grauDificuldade = db.Column(db.String,nullable=False)
    gestor_id = db.Column(db.Integer, db.ForeignKey("tb_gestor.id"))
    preparacao_id = db.Column(db.Integer, db.ForeignKey("tb_preparacao.id"))
    unidade_id = db.Column(db.Integer,db.ForeignKey("tb_unidademedida.id"))
    
    preparacao = db.relationship("Preparacao", uselist=False)
    gestor = db.relationship("Gestor", uselist=False)
    unPesoPorcao = db.relationship("UnidadeMedida",uselist=False)

    def __init__(self, componente, tempoPreparo, numPorcao, custoPreparo, rendimento, pesoPorcao, medidaPorcao, indicadorConversao, fatorCorrecaoGlobal, gestor , preparacao,unPesoPorcao):
        self.componente = componente
        self.tempoPreparo = tempoPreparo
        self.numPorcao = numPorcao
        self.custoPreparo = custoPreparo
        self.custoPorcao = custoPreparo / numPorcao
        self.rendimento = rendimento
        self.pesoPorcao = pesoPorcao
        self.medidaPorcao = medidaPorcao
        self.indicadorConversao = indicadorConversao
        self.fatorCorrecaoGlobal = fatorCorrecaoGlobal
        self.unPesoPorcao = unPesoPorcao
        self.gestor = gestor
        self.preparacao = preparacao

    def __repr__(self):
        return f'<Ficha Tecnica {self.id}>'
=======
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
