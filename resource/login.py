from flask_restful import Resource, reqparse, marshal, fields, Headers
from flask import jsonify
from helpers.logger import logger
from model.mensagem import Message, msgError
from model.usuario import Usuario, userFields
from model.token import Token, tokenFields

from datetime import datetime, timedelta
import jwt
parser = reqparse.RequestParser()

parser.add_argument("email", type=str, help="email nao informado", required=True)
parser.add_argument("senha", type=str, help="senha nao informado", required=True)


class Login(Resource):
  def post(self):
    args = parser.parse_args()
    user = Usuario.query.filter_by(email= args["email"]).first()
    if user is None:
      logger.error(f"Usuario de email: {args['email']} não encontrado")

      codigo = Message(1, f"email:{args['email']} não encontrado")
      return marshal(codigo, msgError), 404
    
    if not user.verify_password(args['senha']):
      token = Token("Senha Incorreta ou inexistente")
      return marshal(token, tokenFields), 404
    
    token = jwt.encode({
      'Tipo': user.tipo,
      'exp': datetime.utcnow() + timedelta(minutes=30)
    }, key='1234', algorithm="HS256")
    return {"token": token}, 200