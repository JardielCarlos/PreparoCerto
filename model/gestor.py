from flask_restful import fields
from helpers.database import db
from model.usuario import Usuario
from sqlalchemy import ForeignKey

userFields = {}

class Gestor(Usuario, db.Model):
  __tablename__ = "tb_gestor"
  __mapper_args__ = {"polymorphic_identity": "gestor"}

  id = db.Column(ForeignKey("tb_usuario.id"), primary_key=True)

  def __init__(self, nome, email, senha):
    super().__init__(nome, email, senha)

  def __repr__(self):
    return f"<Gestor {self.nome}>"