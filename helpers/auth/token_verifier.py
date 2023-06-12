from functools import wraps

from flask_restful import request, marshal

from jwt import decode, InvalidSignatureError, ExpiredSignatureError
from .token_handler import token_creator

from helpers.logger import logger

from model.blackList import BlackList

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
      token = Token("Token invalido")
      return marshal(token, tokenFields), 401
    
    except ExpiredSignatureError:
      token = Token("Token Expirado")
      return marshal(token, tokenFields), 401
    
    except KeyError:
      token = Token("Token com campos faltando")
      return marshal(token, tokenFields), 401
    except IndexError:
      codigo = Message(1, "Schema de autenticação nao informado")
      return marshal(codigo, msgError), 400
    
    blackToken = BlackList.query.filter_by(token=token).first()

    if blackToken:
      token = Token("Token na black list")
      return marshal(token, tokenFields), 401

    next_token = token_creator.refresh(token)
    return function(*args, tipo, next_token, **kwargs)
  
  return decorated