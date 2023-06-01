from flask_restful import fields
from helpers.database import db

preparacaoFields = {'id': fields.Integer, 'nome': fields.String, 'componente': fields.String, 'medidaPorcao': fields.String, 'tempoPreparo': fields.Integer, 'rendimento': fields.Float, 'numPorcao': fields.Float, 'pesoPorcao': fields.Float, 'indicadorConversao': fields.Float, 'fatorCorrecaoGlobal': fields.Float,'custoPreparo': fields.Float,'custoPorcao': fields.Float}

class Preparacao(db.Model):
  __tablename__ = "tb_preparacao"

  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String, nullable=False)
  componente = db.Column(db.String, nullable=False)
  medidaPorcao = db.Column(db.String, nullable=False)
  tempoPreparo = db.Column(db.Integer, nullable=False)
  rendimento = db.Column(db.Float, nullable=False)
  numPorcao = db.Column(db.Float, nullable=False)
  pesoPorcao = db.Column(db.Float, nullable=False)
  indicadorConversao = db.Column(db.Float, nullable=False)
  fatorCorrecaoGlobal = db.Column(db.Float, nullable=False)
  custoPreparo = db.Column(db.Float, nullable=False)
  custoPorcao = db.Column(db.Float, nullable=False)

  def __init__(self, nome, componente, medidaPorcao, tempoPreparo, rendimento, numPorcao, indicadorConversao, fatorCorrecaoGlobal, custoPreparo):
    self.nome = nome
    self.componente = componente
    self.medidaPorcao = medidaPorcao
    self.tempoPreparo = tempoPreparo
    self.rendimento = rendimento
    self.numPorcao = numPorcao
    self.pesoPorcao = rendimento / numPorcao
    self.indicadorConversao = indicadorConversao
    self.fatorCorrecaoGlobal = fatorCorrecaoGlobal
    self.custoPreparo = custoPreparo
    self.custoPorcao = custoPreparo / numPorcao

  def __repr__(self):
    return f'<Preparacao {self}>'