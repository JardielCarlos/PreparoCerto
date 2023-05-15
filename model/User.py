from flask_restful import fields
from helpers.database import db

userFields = {}

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String, nullable=False)
  email = db.Column(db.String, nullable=False, unique=True)
  senha = db.Column(db.String, nullable=False)

  def __init__(self, nome, email, senha):
    self.nome = nome
    self.email = email
    self.senha = senha

  def __repr__(self):
    return f'<User {self.nome}>'