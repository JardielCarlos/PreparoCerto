from flask_restful import Resource, marshal, reqparse
from helpers.database import db
from helpers.logger import logger
from sqlalchemy.exc import IntegrityError

from model.preparador import Preparador, preparadorFields
from model.mensagem import Message, msgFields
from model.empresa import Empresa

from password_strength import PasswordPolicy
import re

parser = reqparse.RequestParser()

parser.add_argument("nome", type=str, help="Nome não informado", required=True)
parser.add_argument("email", type=str, help="Email não informado", required=True)
parser.add_argument("senha", type=str, help="Senha não informada", required=True)
parser.add_argument("empresa", type=dict, help="Empresa não informada", required=False)

padrao_email = r'^[\w\.-]+@[\w\.-]+\.\w+$'
policy = PasswordPolicy.from_names(
  length =8,
  uppercase = 1,
  numbers=1,
  special=1
)

class Preparadores (Resource):
  def get(self):
    preparadores = Preparador.query.all()
    logger.info("Preparadores listados com sucesso")
    return marshal(preparadores, preparadorFields), 200

  def post(self):
    args = parser.parse_args()

    try:

      if len(args['nome']) == 0:
        logger.info("Nome nao informado")

        codigo = Message(1, "Nome nao informado")
        return marshal(codigo, msgFields), 400

      if re.match(padrao_email, args['email']) == None:
        codigo = Message(1, "Email no formato errado")
        return marshal(codigo, msgFields), 400

      verifySenha = policy.test(args['senha'])
      if len(verifySenha) != 0:
        codigo = Message(1, "Senha no formato errado")
        return marshal(codigo, msgFields), 400

      if args['empresa'] == None:
        logger.info("Empresa não informada")
        codigo = Message(1, "Empresa não informada")
        return marshal(codigo, msgFields), 400

      empresaId = args['empresa']['id']
      empresa = Empresa.query.get(empresaId)

      if empresa is None:
        logger.error(f"Empresa de id: {empresaId} não encontrada")

        codigo = Message(1, f"Empresa de id: {empresaId} não encontrada")
        return marshal(codigo, msgFields), 404


      preparador = Preparador(args['nome'], args['email'], args['senha'], empresa)

      db.session.add(preparador)
      db.session.commit()

      logger.info(f"Preparador de id: {preparador.id} criado com sucesso")
      return marshal(preparador, preparadorFields), 201

    except IntegrityError:
      codigo = Message(1, "Email ja cadastrado no sistema")
      return marshal(codigo, msgFields), 400

    except:
      logger.error("Erro ao cadastrar o Preparador")

      codigo = Message(2, "Erro ao cadastrar o Preparador")
      return marshal(codigo, msgFields), 400

class PreparadorId(Resource):
  def get(self, id):
    preparador = Preparador.query.get(id)

    if preparador is None:
      logger.error(f"Preparador de id: {id} não encontrado")

      codigo = Message(1, f"Preparador de id: {id} não encontrado")
      return marshal(codigo, msgFields), 404

    logger.info(f"Preparador de id: {id} listado com sucesso")
    return marshal(preparador, preparadorFields), 200

  def put(self, id):
    args = parser.parse_args()

    try:
      userBd = Preparador.query.get(id)
      if userBd is None:
        logger.error(f"Preparador de id: {id} não encontrado")

        codigo = Message(1, f"Preparador de id: {id} não encontrado")
        return marshal(codigo, msgFields), 404

      if len(args['nome']) == 0:
        logger.info("Nome nao informado")

        codigo = Message(1, "Nome nao informado")
        return marshal(codigo, msgFields), 400

      if re.match(padrao_email, args['email']) == None:
        codigo = Message(1, "Email no formato errado")
        return marshal(codigo, msgFields), 400

      verifySenha = policy.test(args['senha'])
      if len(verifySenha) != 0:
        codigo = Message(1, "Senha no formato errado")
        return marshal(codigo, msgFields), 400

      userBd.nome = args['nome']
      userBd.email = args['email']
      userBd.senha = args['senha']

      db.session.add(userBd)
      db.session.commit()

      logger.info(f"Preparador de id: {id} atualizado com sucesso")
      return marshal(userBd, preparadorFields)

    except:
      logger.error("Erro ao atualizar o Preparador")

      codigo = Message(2, "Erro ao atualizar o Preparador")
      return marshal(codigo, msgFields), 400

  def delete(self, id):
    userBd = Preparador.query.get(id)

    if userBd is None:
      logger.error(f"Preparador de id: {id} não encontrado")

      codigo = Message(1, f"Preparador de id: {id} não encontrado")
      return marshal(codigo, msgFields), 404

    db.session.delete(userBd)
    db.session.commit()

    logger.info(f"Preparador de id: {id} deletado com sucesso")
    return {}, 200
