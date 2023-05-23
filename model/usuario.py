from flask_restful import fields
from helpers.database import db
from sqlalchemy.types import String

userFields = {}

class Usuario(db.Model):
  __tablename__ = "tb_usuario"
  
  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String, nullable=False)
  email = db.Column(db.String, nullable=False, unique=True)
  senha = db.Column(db.String, nullable=False)

  tipo_usuario = db.Column("tipo_usuario", String(50))
  __mapper_args__ = {"polymorphic_on": tipo_usuario}

  def __init__(self, nome, email, senha):
    self.nome = nome
    self.email = email
    self.senha = senha

  def __repr__(self):
    return f"<User {self.nome}>"