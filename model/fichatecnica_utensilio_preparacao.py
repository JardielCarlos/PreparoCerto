from flask_restful import fields
from helpers.database import db
from model.utensilio_preparacao import utensilioPreparacaoFields
from model.ficha_tecnica import fichaTecnicaFields

utensilioPreparacaoFields = {'id': fields.Integer,'fichaTecnica': fields.Nested(fichaTecnicaFields), 'utensilioPreparacao': fields.Nested(utensilioFields)}

class FichaTecnicaUtensilioPreparacao(db.Model):
    __tablename__ = "tb_fichatecnicautensiliopreparacao"

    id = db.Column(db.Integer, primary_key=True)
    fichaTecnica_id = db.Column(db.Integer,db.ForeignKey("tb_fichatecnica"))
    utensilioPreparacao_id = db.Column(db.Integer, db.ForeignKey("tb_utensiliopreparacao.id"))

    fichaTecnica = db.relationship("FichaTecnica", uselist=False)
    utensilioPreparacao = db.relationship("UtensilioPreparacao", uselist=False)

    def __init__(self, utensilio, preparacao):
      self.utensilio = utensilio
      self.preparacao = preparacao

    def __repr__(self):
      return f'<FichaTecnicaUtensilioPreparacao {self.id}>'