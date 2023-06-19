from flask_restful import Resource, reqparse, marshal
from helpers.logger import logger

from model.mensagem import Message, msgError

from model.usuario import Usuario, userEmailFields

class Usuarios(Resource):
    def get(self):
        return marshal(Usuario.query.all(), userEmailFields)
