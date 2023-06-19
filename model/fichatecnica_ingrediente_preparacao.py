from flask_restful import fields
from helpers.database import db
from model.preparacao import preparacaoFields
from model.preparacao_ingrediente import ingredientePreparacaoFields
from model.ficha_tecnica import fichaTecnicaFields

ingredientePreparacaoFields = {'id': fields.Integer,'fichatecnica': fields.Nested(fichaTecnicaFields), 'ingredientePreparacao': fields.Nested(ingredientePreparacaoFields)}

class FichaTecnicaIngredientePreparacao(db.Model):
    __tablename__ = "tb_fichatecnicaingredientepreparacao"

    id = db.Column(db.Integer, primary_key=True)
    fichatecnica_id = db.Column(db.Integer,db.ForeignKey("tb_fichatecnica.id"))
    ingredientePreparacao_id = db.Column(db.Integer, db.ForeignKey("tb_preparacao_ingrediente.id"))

    preparacaoIngrediente = db.relationship("PreparacaoIngrediente", uselist=False)

    def __init__(self, preparacaoIngrediente):
      self.preparacaoIngrediente = preparacaoIngrediente

    def __repr__(self):
      return f'<FichaTecnicaIngredientePreparacao {self.id}>'