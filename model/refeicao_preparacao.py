from flask_restful import fields
from helpers.database import db
from model.preparacao import preparacaoFields
from model.refeicao import refeicaoFields

refeicaoPreparacaoFields = {'id': fields.Integer, 'refeicao': fields.Nested(refeicaoFields), 'preparacao': fields.Nested(preparacaoFields)}

class RefeicaoPreparacao(db.Model):
    __tablename__ = "tb_preparacaorefeicao"

    id = db.Column(db.Integer, primary_key=True)
    refeicao_id = db.Column(db.Integer, db.ForeignKey("tb_refeicao.id"))
    preparacao_id = db.Column(db.Integer, db.ForeignKey("tb_preparacao.id"))

    refeicao = db.relationship("Refeicao", uselist=False)
    preparacao = db.relationship("Preparacao", uselist=False)

    def __init__(self, refeicao, preparacao):
      self.refeicao = refeicao
      self.preparacao = preparacao

    def __repr__(self):
      return f'<PreparacaoRefeicao {self}>'