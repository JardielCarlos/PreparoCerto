from flask_restful import fields
from helpers.database import db

ingredienteFields = {
  'id': fields.Integer,
  'codigo': fields.String,
  'nome': fields.String
}

class Ingrediente(db.Model):
  __tablename__ = 'tb_ingrediente'

  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String, nullable=False)
  codigo = db.Column(db.String, nullable=False)

  def __init__(self, codigo, nome):
   self.codigo = codigo
   self.nome = nome

  def __repr__(self):
    return f'<Ingrediente {self.nome}>'
