from flask_restful import fields
from helpers.database import db
from model.usuario import Usuario


class Preparador(Usuario):
  __tablename__="preparador"

  def __repr__(self):
    return f'<Preparador {self.nome}>'