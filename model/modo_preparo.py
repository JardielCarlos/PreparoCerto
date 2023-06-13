from flask_restful import fields
from helpers.database import db

modoPreparoFields = {
  "id": fields.Integer,
  "text": fields.String
}

class ModoPreparo(db.Model):
  __tablename__ = "tb_modopreparo"    

  id = db.Column(db.Integer, primary_key=True)
  text = db.Column(db.String, nullable=False)

  def __init__(self, text):
    self.text = text

  def __repr__(self):
    return f'ModoPreparo {self.id}'