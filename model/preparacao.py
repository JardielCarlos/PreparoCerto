from flask_restful import fields
from helpers.database import db

preparacaoFields = {}

class Preparacao(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String, nullable=False)
  componente = db.Column(db.String, nullable=False)
  medidaPorcao = db.Column(db.String, nullable=False)
  tempoPreparo = db.Column(db.int, nullable=False)
  rendimento = db.Column(db.float, nullable=False)
  numPorcao = db.Column(db.float, nullable=False)
  pesoPorcao = db.Column(db.float, nullable=False)
  ic = db.Column(db.float, nullable=False)
  fcg = db.Column(db.float, nullable=False)
  custoPreparo = db.Column(db.float, nullable=False)
  custoPorcao = db.Column(db.float, nullable=False)

  def __init__(self, nome, componente, medidaPorcao, tempoPreparo, rendimento, numPorcao, ic, fcg, custoPreparo):
    self.nome = nome
    self.componente = componente
    self.medidaPorcao = medidaPorcao
    self.tempoPreparo = tempoPreparo
    self.rendimento = rendimento
    self.numPorcao = numPorcao
    self.pesoPorcao = rendimento / numPorcao
    self.ic = ic
    self.fcg = fcg
    self.custoPreparo = custoPreparo
    self.custoPorcao = custoPreparo / numPorcao

  def __repr__(self):
    return f'<Preparacao {self}>'