from datetime import datetime
from flask_restful import fields
from helpers.database import db
from model.preparacao import preparacaoFields

modoPreparoFields = {
  "id": fields.Integer,
  "text": fields.String,
  "criacao": fields.DateTime,
  "preparacao": fields.Nested(preparacaoFields)
}

modoPreparoFichaTecnicaFields = {
  "id": fields.Integer,
  "text": fields.String,
}

class ModoPreparo(db.Model):
  __tablename__ = "tb_modopreparo"

  id = db.Column(db.Integer, primary_key=True)
  text = db.Column(db.Text, nullable=False)
  criacao = db.Column(db.DateTime, default=datetime.utcnow)
  is_deleted = db.Column(db.Boolean, default=False)

  preparacao_id = db.Column(db.Integer, db.ForeignKey('tb_preparacao.id'))

  # Preparação
  preparacao = db.relationship("Preparacao")

  def __init__(self, text, preparacao):
    self.text = text
    self.preparacao = preparacao

  def __repr__(self):
    return f'ModoPreparo {self.id}'
