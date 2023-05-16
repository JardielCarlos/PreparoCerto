from flask_restful import fields
from helpers.database import db

empresaFields = {}

class Empresa(db.Model):
  __tablename__="empresa"
  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String, nullable=False)
  cnpj = db.Column(db.String, nullable=False, unique=True)
  gestor_id = db.Column(db.Integer,nullable=False,db.Foreingkey('gestor.id'))

  def __init__(self, nome, cnpj):
    self.nome = nome
    self.cnpj = cnpj

  def __repr__(self):
    return f'<Empresa {self.nome}>'