from flask_restful import fields
from helpers.database import db
from model.usuario import Usuario
from model.empresa import empresaFields

gestorFields = {'id': fields.Integer, 'nome': fields.String, 'email': fields.String, 'senha': fields.String, "empresa": fields.Nested(empresaFields)}

class Gestor(Usuario):
  __tablename__ = "tb_gestor"

  usuario_id = db.Column(db.Integer ,db.ForeignKey("tb_usuario.id"), primary_key=True)
  empresa_id =  db.Column(db.Integer ,db.ForeignKey("tb_empresa.id"))

  empresa = db.relationship("Empresa", uselist=False)

  __mapper_args__ = {"polymorphic_identity": "gestor"}

  def __init__(self, nome, email, senha, empresa):
    super().__init__(nome, email, senha)
    self.empresa = empresa

  def __repr__(self):
    return f"<Gestor {self.nome}>"