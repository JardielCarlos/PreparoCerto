from flask_restful import fields
from helpers.database import db
from model.empresa import empresaFields

cardapioFields = {
  'id': fields.Integer,
  'empresa': fields.Nested(empresaFields)
  }

class Cardapio(db.Model):
  __tablename__="tb_cardapio"

  id = db.Column(db.Integer, primary_key=True)
  empresa_id = db.Column(db.Integer ,db.ForeignKey("tb_empresa.id"))

  empresa = db.relationship("Empresa", uselist=False)

  def __init__(self, empresa):
    self.empresa = empresa

  def __repr__(self):
    return f'<Cardapio {self.nome}>'
