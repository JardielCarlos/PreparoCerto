import datetime
from flask_restful import fields
from helpers.database import db
from model.empresa import empresaFields

preparacaoFields = {
    'id': fields.Integer,
    'nome': fields.String,
    "criacao": fields.DateTime,
    'empresa': fields.Nested(empresaFields)
}


class Preparacao(db.Model):
    __tablename__ = "tb_preparacao"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    criacao = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    empresa_id = db.Column(db.Integer, db.ForeignKey("tb_empresa.id"))

    # Empresa
    empresa = db.relationship("Empresa", uselist=False)

    def __init__(self, nome, empresa):
        self.nome = nome
        self.empresa = empresa

    def __repr__(self):
        return f'<Preparacao {self.nome}>'
