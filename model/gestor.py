from flask_restful import fields
from helpers.database import db
from model.usuario import Usuario
userFields = {}

class Gestor(Usuario):
  __tablename__="gestor"

  def __repr__(self):
    return f'<Gestor {self.nome}>'