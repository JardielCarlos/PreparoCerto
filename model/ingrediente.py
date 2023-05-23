from flask_restful import fields
from helpers.database import db

ingredientsFields = {'id': fields.Integer, 'nome': fields.String, 'pb': fields.Float, 'un': fields.Float, 'ipc': fields.Float, 'pl': fields.Float, 'pc': fields.Float, 'embalagem': fields.Float, 'preco': fields.Float, 'custPrep': fields.Float}

class Ingrediente(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String, nullable=False)
  pb = db.Column(db.float, nullable=False)
  un = db.Column(db.float, nullable=False)
  ipc = db.Column(db.float, nullable=False)
  pl = db.Column(db.float,nullable=False)
  pc = db.Column(db.float, nullable=False)
  embalagem = db.Column(db.float, nullable=False)
  preco = db.Column(db.float, nullable=False)
  custPrep = db.Column(db.float, nullable=False)

  def __init__(self, nome, pb, un, ipc, pl, pc, embalagem, preco, custPrep):
    self.nome = nome
    self.pb = pb
    self.un = un
    self.ipc = ipc
    self.pl = pl
    self.pc = pc
    self.embalagem = embalagem
    self.preco = preco
    self.custPrep = custPrep

  def __repr__(self):
    return f'<Ingrediente {self}>'