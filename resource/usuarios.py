from flask_restful import Resource

class Usuarios(Resource):
  def get(self):
    return {'hello': 'world'}