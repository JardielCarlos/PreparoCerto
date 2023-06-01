from flask_restful import fields
from helpers.database import db

refeicaoFields = {'id': fields.Integer, 'nome': fields.String}

class Refeicao(db.Model):
    __tablename__ = "tb_refeicao"
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String,nullable=False)

    def __init__(self, nome):
      self.nome = nome

    def __repr__(self):
      return f"<Refeicao {self}>"