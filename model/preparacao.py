from flask_restful import fields
from helpers.database import db
from model.empresa import empresaFields
from model.modo_preparo import modoPreparoFields

preparacaoFields = {
  'id': fields.Integer,
  'nome': fields.String,
  'empresa': fields.Nested(empresaFields),
  'modoPreparo': fields.Nested(modoPreparoFields)
  }

class Preparacao(db.Model):
  __tablename__ = "tb_preparacao"

  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String, nullable=False)
  empresa_id = db.Column(db.Integer, db.ForeignKey("tb_empresa.id"))
  modoPreparo_id = db.Column(db.Integer, db.ForeignKey("tb_modopreparo.id"))

  empresa = db.relationship("Empresa", uselist=False)
  modoPreparo = db.relationship("ModoPreparo", uselist=False)

  def __init__(self, nome, empresa, modoPreparo):
    self.nome = nome
    self.empresa = empresa
    self.modoPreparo = modoPreparo

  def __repr__(self):
    return f'<Preparacao {self.nome}>'
