from datetime import datetime
from flask_restful import fields
from helpers.database import db
from model.preparacao import preparacaoFields

modoPreparoFields = {
  "id": fields.Integer,
  "text": fields.String,
  "criacao": fields.String,
  "preparacao": fields.Nested(preparacaoFields)
}

modoPreparoTokenFields ={
  'modoPreparo': fields.Nested(modoPreparoFields),
  'token': fields.String
}

modoPreparoFichaTecnicaFields = {
  "id": fields.Integer,
  "text": fields.String,
}

modoPreparoFichaTecnicaTokenFields = {
  'modoPrepFicha': fields.Nested(modoPreparoFichaTecnicaFields),
  'token': fields.String
}

class ModoPreparo(db.Model):
  __tablename__ = "tb_modopreparo"

  id = db.Column(db.Integer, primary_key=True)
  text = db.Column(db.Text, nullable=False)
  criacao = db.Column(db.DateTime, default=datetime.utcnow)

  preparacao_id = db.Column(db.Integer, db.ForeignKey('tb_preparacao.id'))

  # Preparação
  preparacao = db.relationship("Preparacao", backref= db.backref("tb_modopreparo", cascade="all, delete"))

  def __init__(self, text, preparacao):
    self.text = text
    self.preparacao = preparacao

  def __repr__(self):
    return f'ModoPreparo {self.id}'
