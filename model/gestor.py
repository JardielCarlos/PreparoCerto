from flask_restful import fields
from helpers.database import db

userFields = {}

class Gestor(user.User):
  __tablename__="gestor"

  def __repr__(self):
    return f'<Gestor {self.nome}>'