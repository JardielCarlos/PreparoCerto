from flask_restful import fields
from helpers.database import db
from model.empresa import empresaFields

cardapioFields = {
  'id': fields.Integer,
  'nome': fields.String,
  'empresa': fields.Nested(empresaFields)
  }

class Cardapio(db.Model):
  __tablename__="tb_cardapio"

  id = db.Column(db.Integer, primary_key=True)
  empresa_id = db.Column(db.Integer ,db.ForeignKey("tb_empresa.id"))

  empresa = db.relationship("Empresa", uselist=False)

  def __init__(self, nome, empresa):
    self.nome = nome
    self.empresa = empresa

  def __repr__(self):
    return f'<Cardapio {self.nome}>'
