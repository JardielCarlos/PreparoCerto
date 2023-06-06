from flask_restful import fields
from helpers.database import db

cardapioFields = {'id': fields.Integer, 'sigla': fields.String}

class Unidade(db.Model):
  __tablename__="tb_unidade"

  id = db.Column(db.Integer, primary_key=True)
  sigla = db.Column(db.String, nullable=False)

  def __init__(self, sigla):
    self.sigla = sigla

  def __repr__(self):
    return f'<Unidade {self.sigla}>'