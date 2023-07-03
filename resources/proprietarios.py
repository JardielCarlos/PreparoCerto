from flask_restful import Resource, reqparse, marshal
from helpers.database import db
from helpers.auth.token_verifier import token_verify
from helpers.logger import logger
from sqlalchemy.exc import IntegrityError
from password_strength import PasswordPolicy
import re

from model.usuario import userTokenFields
from model.mensagem import Message, msgFields
from model.proprietario import Proprietario

parser = reqparse.RequestParser()

parser.add_argument("nome", type=str, help="Nome não informado", required=True)
parser.add_argument("email", type=str, help="Email não informado", required=True)
parser.add_argument("senha", type=str, help="Senha não informado", required=False)

padrao_email = r'^[\w\.-]+@[\w\.-]+\.\w+$'
policy = PasswordPolicy.from_names(
  length =8,
  uppercase = 1,
  numbers=1,
  special=1
)

class Proprietarios(Resource):
  @token_verify
  def get(self, tipo, refreshToken):
    if tipo != 'proprietario':
      logger.error("Usuario sem autorizacao para acessar os proprietarios")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403
    proprietarios = Proprietario.query.all()

    data = {'user': proprietarios, 'token': refreshToken}

    logger.info("Proprietarios listados com sucesso")
    return marshal(data, userTokenFields), 200

  @token_verify
  def post(self, tipo, refreshToken):
    args = parser.parse_args()

    try:
      if len(args['nome']) == 0:
        logger.info("Nome nao informado")

        codigo = Message(1, "Nome nao informado")
        return marshal(codigo, msgFields), 400

      if re.match(padrao_email, args['email']) == None:
        codigo = Message(1, "Email no formato errado")
        return marshal(codigo, msgFields), 400

      if not args['senha']:
        codigo = Message(1, "Senha não informada")
        return marshal(codigo, msgFields), 400

      verifySenha = policy.test(args['senha'])
      if len(verifySenha) != 0:
        codigo = Message(1, "Senha no formato errado")
        return marshal(codigo, msgFields), 400

      proprietario = Proprietario(args['nome'], args["email"], args['senha'])

      db.session.add(proprietario)
      db.session.commit()

      data = {'user': proprietario, 'token': refreshToken}

      logger.info(f"Proprietário de id: {proprietario.id} criado com sucesso")
      return marshal(data, userTokenFields), 201

    except IntegrityError:
      codigo = Message(1, "Email ja cadastrado no sistema")
      return marshal(codigo, msgFields)
    except:
      logger.error("Error ao cadastrar o Proprietário")

      codigo = Message(2, "Error ao cadastrar o Proprietário")
      return marshal(codigo, msgFields), 400

class ProprietarioId(Resource):
  @token_verify
  def get(self, tipo, refreshToken, id):
    if tipo != 'proprietario':
      logger.error("Usuario sem autorizacao para acessar os proprietarios")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

    proprietario = Proprietario.query.get(id)

    if proprietario is None:
      logger.error(f"Proprietário de id: {id} não encontrado")

      codigo = Message(1, f"Proprietário de id: {id} não encontrado")
      return marshal(codigo, msgFields), 404

    data = {'user': proprietario, 'token': refreshToken}


    logger.info(f"Proprietário de id: {proprietario.id} listado com Sucesso")
    return marshal(data, userTokenFields), 200

  @token_verify
  def put(self, tipo, refreshToken, id):
    if tipo != 'proprietario':
      logger.error("Usuario sem autorizacao para acessar os proprietarios")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

    args = parser.parse_args()

    try:
      userBd = Proprietario.query.get(id)
      if userBd is None:
        logger.error(f"Proprietário de id: {id} não encontrado")

        codigo = Message(1, f"Proprietário de id: {id} não encontrado")
        return marshal(codigo, msgFields), 404

      if len(args['nome']) == 0:
        logger.info("Nome nao informado")

        codigo = Message(1, "Nome nao informado")
        return marshal(codigo, msgFields), 400

      if re.match(padrao_email, args['email']) == None:
        codigo = Message(1, "Email no formato errado")
        return marshal(codigo, msgFields), 400


      userBd.nome = args["nome"]
      userBd.email = args["email"]

      db.session.add(userBd)
      db.session.commit()

      data = {'user': userBd, 'token': refreshToken}


      logger.info(f"Proprietário de id: {id} atualizado com Sucesso")
      return marshal(data, userTokenFields), 200

    except:
      logger.error("Error ao atualizar o Proprietário")

      codigo = Message(2, "Error ao atualizar o Proprietario")
      return marshal(codigo, msgFields), 400
  @token_verify
  def delete(self, tipo, refreshToken, id):
    if tipo != 'proprietario':
      logger.error("Usuario sem autorizacao para acessar os proprietarios")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

    try:
      userBd = Proprietario.query.get(id)

      if userBd is None:
        logger.error(f"Proprietário de id: {id} não encontrado")

        codigo = Message(1, f"Proprietário de id: {id} não encontrado")
        return marshal(codigo, msgFields), 404

      db.session.delete(userBd)
      db.session.commit()

      logger.info(f"Proprietário de id: {id} deletado com sucesso")
      return {'token': refreshToken}, 200

    except IntegrityError:
      logger.error(f"Proprietário de id: {id} não pode ser deletado possui dependencia com a empresa")

      codigo = Message(1, f"Proprietário de id: {id} não pode ser deletado possui empresa cadastrada")
      return marshal(codigo, msgFields), 400
class ProprietarioNome(Resource):
  @token_verify
  def get(self, tipo, refreshToken,  nome):
    if tipo != 'proprietario':
      logger.error("Usuario sem autorizacao para acessar os proprietarios")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

    proprietarioNome = Proprietario.query.filter(Proprietario.nome.ilike(f'%{nome}%')).all()

    data = {'user': proprietarioNome, 'token': refreshToken}

    logger.info(f"Proprietarios com nome: {nome} listado com sucesso")
    return marshal(data, userTokenFields), 200

