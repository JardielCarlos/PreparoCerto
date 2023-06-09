from flask_restful import fields
from helpers.database import db
from model.usuario import Usuario

proprietarioFields = {
  'id': fields.Integer,
  'nome': fields.String,
  'email': fields.String,
  'senha': fields.String,
  }

class Proprietario(Usuario):
  __tablename__ = "tb_proprietario"

  usuario_id = db.Column(db.Integer ,db.ForeignKey("tb_usuario.id"), primary_key=True)

  __mapper_args__ = {"polymorphic_identity": "proprietario"}

  def __init__(self, nome, email, senha):
    super().__init__(nome, email, senha)
    

  def __repr__(self):
    return f"<Proprietario {self.nome}>"