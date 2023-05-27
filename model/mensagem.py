from flask_restful import fields

msgError = {"codigo": fields.Integer, "descricao": fields.String}

class Message:
  def __init__(self, codigo, descricao):
    self.codigo = codigo
    self.descricao = descricao
