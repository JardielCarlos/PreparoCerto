from flask_restful import fields
from helpers.database import db

unidadeFields = {'id': fields.Integer, 'nome': fields.String, 'sigla': fields.String}

class UnidadeMedida(db.Model):
  __tablename__ = "tb_unidademedida"
  
  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String, nullable=False)
  sigla = db.Column(db.String, nullable=False, unique=True)

  def __init__(self, nome, sigla):
    self.nome = nome
    self.sigla = sigla

  def __repr__(self):
    return f"<Unidade de Medida {self.nome}>"