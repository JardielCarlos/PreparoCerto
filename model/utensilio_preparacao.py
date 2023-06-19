from flask_restful import fields
from helpers.database import db
from model.preparacao import preparacaoFields
from model.utensilio import utensilioFields

utensilioPreparacaoFields = {
  'id': fields.Integer,
  'utensilio': fields.Nested(utensilioFields),
  'preparacao': fields.Nested(preparacaoFields)
  }

class UtensilioPreparacao(db.Model):
    __tablename__ = "tb_utensiliopreparacao"

    id = db.Column(db.Integer, primary_key=True)
    utensilio_id = db.Column(db.Integer, db.ForeignKey("tb_utensilio.id"))
    preparacao_id = db.Column(db.Integer, db.ForeignKey("tb_preparacao.id"))

    utensilio = db.relationship("Utensilio", uselist=False)
    preparacao = db.relationship("Preparacao", uselist=False)

    def __init__(self, utensilio, preparacao):
      self.utensilio = utensilio
      self.preparacao = preparacao

    def __repr__(self):
      return f'<utensilioPreparacao {self.id}>'
