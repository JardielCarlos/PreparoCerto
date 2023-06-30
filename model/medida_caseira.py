from flask_restful import fields
from helpers.database import db

medidaCaseiraFields = {
  'id': fields.Integer,
  'quantidade': fields.String,
  'descricao': fields.String
}

class MedidaCaseira(db.Model):
  __tablename__ = "tb_medidacaseira"

  id = db.Column(db.Integer, primary_key=True)
  quantidade = db.Column(db.String, nullable=False)
  descricao = db.Column(db.String, nullable=False, unique=True)

  def __init__(self, quantidade, descricao):
    self.quantidade = quantidade
    self.descricao = descricao

  def __repr__(self):
    return f"<Unidade de Medida {self.id}>"
