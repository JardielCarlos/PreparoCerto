from flask_restful import fields
from helpers.database import db

ingredienteFields = {'id': fields.Integer, 'nome': fields.String, 'pesoBruto': fields.Float, 'unidade': fields.String, 'indicadorParteComestivel': fields.Float, 'pesoLiquido': fields.Float, 'perCapita': fields.Float, 'embalagem': fields.Float, 'preco': fields.Float, 'custPreparacao': fields.Float}

class Ingrediente(db.Model):
  __tablename__ = 'tb_ingrediente'
  
  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String, nullable=False)
  pesoBruto = db.Column(db.Float, nullable=False)
  unidade = db.Column(db.String, nullable=False)
  indicadorParteComestivel = db.Column(db.Float, nullable=False)
  pesoLiquido = db.Column(db.Float,nullable=False)
  perCapita = db.Column(db.Float, nullable=False)
  embalagem = db.Column(db.Float, nullable=False)
  preco = db.Column(db.Float, nullable=False)
  custPreparacao = db.Column(db.Float, nullable=False)

  def __init__(self, nome, pesoBruto, unidade, indicadorParteComestivel, pesoLiquido, perCapita, embalagem, preco, custPreparacao):
   self.nome = nome
   self.pesoBruto = pesoBruto
   self.unidade = unidade
   self.indicadorParteComestivel = indicadorParteComestivel
   self.pesoLiquido = pesoLiquido
   self.perCapita = perCapita
   self.embalagem = embalagem
   self.preco = preco
   self.custPreparacao = custPreparacao

  def __repr__(self):
    return f'<Ingrediente {self}>'
