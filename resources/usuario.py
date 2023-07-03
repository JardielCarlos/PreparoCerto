from flask_restful import Resource, marshal

from model.usuario import Usuario, userEmailFields

class Usuarios(Resource):
  def get(self):
    return marshal(Usuario.query.all(), userEmailFields)
