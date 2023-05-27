from flask_restful import fields
from helpers.database import db
from model.usuario import Usuario


class Preparador(Usuario):

  __tablename__="preparador"

  usuario_id = db.Column(db.Integer, db.ForeignKey("tb_usuario.id"),primary_key=True)

  __mapper_args__ = {"polymorphic_identity": "preparador"}

  def __init__(self, nome, email, senha):
    super().__init__(nome, email, senha)
    
  def __repr__(self):
    return f'<Preparador {self.nome}>'