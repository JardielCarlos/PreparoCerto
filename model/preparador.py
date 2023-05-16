from flask_restful import fields
from helpers.database import db

userFields = {}

class Preparador(user.User):
  __tablename__="preparador"

  def __repr__(self):
    return f'<Preparador {self.nome}>'