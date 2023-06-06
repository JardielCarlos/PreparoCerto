from flask_restful import request, marshal
from helpers.logger import logger
from model.mensagem import Message, msgError
from model.token import Token, tokenFields

from jwt import decode, InvalidSignatureError, ExpiredSignatureError

def validation(tokenAuthorization):
  if not tokenAuthorization:
    logger.error("Sem token!")

    codigo = Message(1, "Sem token!")
    return marshal(codigo, msgError), 401

  try:
    token = tokenAuthorization.split()[1]
    informationToken = decode(token, key="1234", algorithms="HS256")

    if informationToken['Tipo'] != 'proprietario':
      logger.error("Usuario sem autorização suficiente!")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgError), 403
  except InvalidSignatureError:
    token = Token("Token invalido!")
    return marshal(token, tokenFields), 401

  except ExpiredSignatureError:
    token = Token("Token Expirado!")

    return marshal(token, tokenFields), 401