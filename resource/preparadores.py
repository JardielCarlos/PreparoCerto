from flask_restful import Resource, marshal
from model.preparador import Preparador
from model.usuario import userFields
from helpers.database import db

class Preparadores (Resource):
  def get(self):
    return marshal(Preparador.query.all(), userFields), 200
  
  def post(self):
    preparador = Preparador("Lais", "lais@gmail.com", "noah")

    db.session.add(preparador)
    db.session.commit()

    return marshal(preparador, userFields), 201