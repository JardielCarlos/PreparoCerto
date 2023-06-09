from flask_restful import fields
from helpers.database import db
from model.preparacao import preparacaoFields
from model.cardapio import cardapioFields

cardapioPreparacaoFields = {
  'id': fields.Integer,
  'cardapio': fields.Nested(cardapioFields),
  'preparacao': fields.Nested(preparacaoFields)
  }

class CardapioPreparacao(db.Model):
    __tablename__ = "tb_cardapiopreparacao"

    id = db.Column(db.Integer, primary_key=True)
    cardapio_id = db.Column(db.Integer, db.ForeignKey("tb_cardapio.id"))
    preparacao_id = db.Column(db.Integer, db.ForeignKey("tb_preparacao.id"))

    cardapio = db.relationship("Cardapio", uselist=False)
    preparacao = db.relationship("Preparacao", uselist=False)

    def __init__(self, cardapio, preparacao):
      self.cardapio = cardapio
      self.preparacao = preparacao

    def __repr__(self):
      return f'<CardapioPreparacao {self.id}>'