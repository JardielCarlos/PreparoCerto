from flask_restful import fields
from helpers.database import db

fichaTecnicaFields = {}

class FichaTecnica(db.Model):
  __tablename__ = "tb_fichatecnica"

  id = db.Column(db.Integer, primary_key=True)
  preparacao_id = db.Column(db.Integer, db.ForeignKey("tb_preparacao.id"))
                                                                   
  preparacao = db.relationship("Preparacao", uselist=False)


  def __init__(self, preparacao,):
      self.preparacao = preparacao


  def __repr__(self):
      return f'<FichaTecnica {self}>'