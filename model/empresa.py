from flask_restful import fields
from helpers.database import db

empresaFields = {'id': fields.Integer, 'nome': fields.String, 'cnpj': fields.String, 'id_proprietario': fields.Integer}

class Empresa(db.Model):
  __tablename__="tb_empresa"

  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String, nullable=False)
  cnpj = db.Column(db.String, nullable=False, unique=True)
  id_proprietario = db.Column(db.Integer, db.ForeignKey("tb_gestor.usuario_id"))

  def __init__(self, nome, cnpj, id_proprietario):
    self.nome = nome
    self.cnpj = cnpj
    self.id_proprietario = id_proprietario

  def __repr__(self):
    return f'<Empresa {self.nome}>'