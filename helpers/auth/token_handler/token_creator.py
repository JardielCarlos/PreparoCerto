from jwt import encode, decode
from datetime import datetime, timedelta
import time

class TokenCreator:
  def __init__(self, token_key: str, exp_time_min: int, refresh_time_min: int):
    self.__TOKEN_KEY =token_key
    self.__EXP_TIME_MIN = exp_time_min
    self.__REFRESH_TIME_MIN = refresh_time_min

  def create(self, tipo: str):
    return self.__encode_token(tipo)
  
  def refresh(self, token: str):
    informationToken = decode(token, key=self.__TOKEN_KEY, algorithms="HS256")
    tipo = informationToken["tipo"]
    exp_time = informationToken["exp"]
    if((exp_time - time.time()) / 60) < self.__REFRESH_TIME_MIN:
      return self.__encode_token(tipo)
    
    return token

  def __encode_token(self, tipo: str):
    token = encode({
      'tipo': tipo,
      'exp': datetime.utcnow() + timedelta(minutes=self.__EXP_TIME_MIN)
    }, key=self.__TOKEN_KEY, algorithm="HS256")

    return token