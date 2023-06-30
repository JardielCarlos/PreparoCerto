import datetime
from flask_restful import fields
from helpers.database import db
from model.empresa import empresaFields

preparacaoFields = {
  'id': fields.Integer,
  'nome': fields.String,
  'numPorcoes': fields.Float,
  "criacao": fields.String,
  'empresa': fields.Nested(empresaFields)
}


class Preparacao(db.Model):
  __tablename__ = "tb_preparacao"

  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String, nullable=False)
  criacao = db.Column(db.DateTime, default=datetime.datetime.now)
  numPorcoes = db.Column(db.Float, nullable=False)
  empresa_id = db.Column(db.Integer, db.ForeignKey("tb_empresa.id"))
  fotoPerfil_id = db.Column(db.Integer, db.ForeignKey("tb_imgpreparacao.id"))

  # Empresa
  empresa = db.relationship("Empresa", uselist=False, backref= db.backref("tb_preparacao", cascade="all, delete"))
  fotoPerfil = db.relationship("ImgPreparacao",uselist=False)

  def __init__(self, nome, numPorcoes, empresa, fotoPerfil):
    self.nome = nome
    self.numPorcoes = numPorcoes
    self.empresa = empresa
    self.fotoPerfil = fotoPerfil

  def __repr__(self):
    return f'<Preparacao {self.nome}>'
