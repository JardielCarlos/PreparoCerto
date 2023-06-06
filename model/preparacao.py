from flask_restful import fields
from helpers.database import db

fichaTecnicaFields = {}

class Preparacao(db.Model):
  __tablename__ = "tb_preparacao"

  id = db.Column(db.Integer, primary_key=True)
  unidade_id = db.Column(db.Integer, db.ForeignKey("tb_unidade.id"))
  medidaCaseira_id = db.Column(db.Integer, db.ForeignKey("tb_medidacaseira.id"))
  estoque_id = db.Column(db.Integer, db.ForeignKey("tb_estoque.id"))

  pesoBruto = db.Column(db.float, nullable=False)
  pesoLiquido = db.Column(db.float, nullable=False)
  indicadorParteComestivel = db.Column(db.float, nullable=False)
  rendimento = db.Column(db.float, nullable=False)
  perCapita = db.Column(db.float, nullable=False)
  tempoPrePreparo = db.Column(db.int, nullable=False)
  tempoPreparo = db.Column(db.int, nullable=False)
  tempoTotal = db.Column(db.int, nullable=False)
  pesoBrutoExplosao = db.Column(db.float, nullable=False)
  pesoLiquidoExplosao = db.Column(db.float, nullable=False)

  unidade = db.relationship("Unidade", uselist=False)
  medidaCaseira = db.relationship("MedidaCaseira", uselist=False)
  estoque = db.relationship("Estoque", uselist=False)

  def __init__(self, unidade, medidaCaseira, estoque, pesoBruto, pesoLiquido, indicadorParteComestivel, rendimento, perCapita, tempoPrePreparo, tempoPreparo, pesoBrutoExplosao, pesoLiquidoExplosao):
      self.unidade = unidade
      self.medidaCaseira = medidaCaseira
      self.estoque = estoque
      self.pesoBruto = pesoBruto
      self.pesoLiquido = pesoLiquido
      self.indicadorParteComestivel = indicadorParteComestivel
      self.rendimento = rendimento
      self.perCapita = perCapita
      self.tempoPrePreparo = tempoPrePreparo
      self.tempoPreparo = tempoPreparo
      self.tempoTotal = tempoPrePreparo + tempoPreparo
      self.pesoBrutoExplosao = pesoBrutoExplosao
      self.pesoLiquidoExplosao = pesoLiquidoExplosao

  def __repr__(self):
      return f'<Preparacao {self}>'