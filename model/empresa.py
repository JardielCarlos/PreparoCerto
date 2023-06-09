from flask_restful import fields
from helpers.database import db
from model.usuario import userFields

empresaFields = {
  'id': fields.Integer,
  'nome': fields.String,
  'cnpj': fields.String,
  'proprietario': fields.Nested(userFields)
  }

class Empresa(db.Model):
  __tablename__="tb_empresa"

  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String, nullable=False)
  cnpj = db.Column(db.String, nullable=False, unique=True)
  proprietario_id = db.Column(db.Integer, db.ForeignKey("tb_proprietario.usuario_id"))

  proprietario = db.relationship("Proprietario", uselist=False)

  def __init__(self, nome, cnpj, proprietario):
    self.nome = nome
    self.cnpj = cnpj
    self.proprietario = proprietario

  def __repr__(self):
    return f'<Empresa {self.nome}>'