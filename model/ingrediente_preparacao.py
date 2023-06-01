from flask_restful import fields
from helpers.database import db
from model.ingrediente import ingredienteFields
from model.preparacao import preparacaoFields

ingredientePreparacaoFields = {'id': fields.Integer, 'ingrediente': fields.Nested(ingredienteFields), 'preparacao': fields.Nested(preparacaoFields)}

class IngredientePreparacao(db.Model):
    __tablename__ = "tb_ingredientepreparacao"

    id = db.Column(db.Integer, primary_key=True)
    ingrediente_id = db.Column(db.Integer, db.ForeignKey("tb_ingrediente.id"))
    preparacao_id = db.Column(db.Integer, db.ForeignKey("tb_preparacao.id"))

    ingrediente = db.relationship("Ingrediente", uselist=False)
    preparacao = db.relationship("Preparacao", uselist=False)

    def __init__(self, ingrediente, preparacao):
      self.ingrediente = ingrediente
      self.preparacao = preparacao

    def __repr__(self):
      return f'<IngredientePreparacao {self}>'