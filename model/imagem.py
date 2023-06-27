from flask_restful import fields
from helpers.database import db

imagemFields = {
  "id": fields.Integer,
  "imagem": fields.String
  }

class Imagem(db.Model):
  __tablename__ = 'tb_imagem'
  
  id = db.Column(db.Integer, primary_key=True)
  imagem = db.Column(db.LargeBinary)
  
  def __init__(self, imagem):
    self.imagem = imagem
