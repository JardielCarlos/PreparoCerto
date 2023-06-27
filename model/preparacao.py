import datetime
from flask_restful import fields
from helpers.database import db
from model.empresa import empresaFields
from model.imagem import imagemFields

preparacaoFields = {
    'id': fields.Integer,
    'nome': fields.String,
    'numPorcoes': fields.Float,
    "criacao": fields.DateTime,
    'empresa': fields.Nested(empresaFields),
    "imagem": fields.Nested(imagemFields)
}


class Preparacao(db.Model):
    __tablename__ = "tb_preparacao"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    criacao = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    numPorcoes = db.Column(db.Float, nullable=False)
    empresa_id = db.Column(db.Integer, db.ForeignKey("tb_empresa.id"))
    imagem_id = db.Column(db.Integer,db.ForeignKey("tb_imagem.id"))

    # Empresa
    empresa = db.relationship("Empresa", uselist=False)
    imagem = db.relationship("Imagem",uselist=False)

    def __init__(self, nome, numPorcoes, empresa, imagem):
        self.nome = nome
        self.numPorcoes = numPorcoes
        self.empresa = empresa
        self.imagem = imagem

    def __repr__(self):
        return f'<Preparacao {self.nome}>'
