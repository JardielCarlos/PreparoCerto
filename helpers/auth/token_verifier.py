from functools import wraps
from flask_restful import request, marshal
from jwt import decode, InvalidSignatureError, ExpiredSignatureError
from .token_handler import token_creator

from helpers.logger import logger

from model.mensagem import Message, msgError
from model.token import Token, tokenFields

def token_verify(function: callable) -> callable:
    
  @wraps(function)
  def decorated(*args, **kwargs):
    rawToken = request.headers["Authorization"]
    if not rawToken:
      logger.error("Sem token!")

      codigo = Message(1, "Sem token!")
      return marshal(codigo, msgError), 401
    
    try:
      token = rawToken.split()[1]
      informationToken = decode(token, key="1234", algorithms="HS256")
      tipo = informationToken['tipo']
      
    except InvalidSignatureError:
      token = Token("Token invalido!")
      return marshal(token, tokenFields), 401
    
    except ExpiredSignatureError:
      token = Token("Token Expirado!")

      return marshal(token, tokenFields), 401
    
    except KeyError as e:
      token = Token("Token com campos faltando!")
      return marshal(token. tokenFields), 401

    if tipo != 'proprietario':
        logger.error("Usuario sem autorização suficiente!")

        codigo = Message(1, "Usuario sem autorização suficiente!")
        return marshal(codigo, msgError), 403
    
    next_token = token_creator.refresh(token)

    return function(next_token, *args, **kwargs)
  
  return decorated