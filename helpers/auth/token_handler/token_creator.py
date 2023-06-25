from jwt import encode, decode
from datetime import datetime, timedelta
import time

class TokenCreator:
  def __init__(self, token_key: str, exp_time_hrs: int, refresh_time_hrs: int):
    self.__TOKEN_KEY =token_key
    self.__EXP_TIME_HRS = exp_time_hrs
    self.__REFRESH_TIME_HRS = refresh_time_hrs

  def create(self, tipo: str):
    return self.__encode_token(tipo)

  def refresh(self, token: str):
    informationToken = decode(token, key=self.__TOKEN_KEY, algorithms="HS256")
    tipo = informationToken["tipo"]
    exp_time = informationToken["exp"]
    
    if((exp_time - time.time()) / 3600) < self.__REFRESH_TIME_HRS:
      return self.__encode_token(tipo)

    return token

  def __encode_token(self, tipo: str):
    token = encode({
      'tipo': tipo,
      'exp': datetime.utcnow() + timedelta(hours=self.__EXP_TIME_HRS)
    }, key=self.__TOKEN_KEY, algorithm="HS256")

    return token
