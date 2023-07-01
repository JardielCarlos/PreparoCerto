from flask_restful import Resource, reqparse, marshal
from helpers.database import db
from model.proprietario import Proprietario
from model.usuario import userFields
from helpers.logger import logger
from model.mensagem import Message, msgFields
from sqlalchemy.exc import IntegrityError
from password_strength import PasswordPolicy
import re

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
  def get(self):
    proprietarios = Proprietario.query.all()

    logger.info("Proprietários listados com sucesso")
    return marshal(proprietarios, userFields), 200

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

      logger.info(f"Proprietário de id: {proprietario.id} criado com sucesso")
      return marshal(proprietario, userFields), 201

    except IntegrityError:
      codigo = Message(1, "Email ja cadastrado no sistema")
      return marshal(codigo, msgFields)
    except:
      logger.error("Error ao cadastrar o Proprietário")

      codigo = Message(2, "Error ao cadastrar o Proprietário")
      return marshal(codigo, msgFields), 400

class ProprietarioId(Resource):
  def get(self, id):
    proprietario = Proprietario.query.get(id)

    if proprietario is None:
      logger.error(f"Proprietário de id: {id} não encontrado")

      codigo = Message(1, f"Proprietário de id: {id} não encontrado")
      return marshal(codigo, msgFields), 404

    logger.info(f"Proprietário de id: {proprietario.id} listado com Sucesso")
    return marshal(proprietario, userFields), 200

  def put(self, id):
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

      logger.info(f"Proprietário de id: {id} atualizado com Sucesso")
      return marshal(userBd, userFields), 200

    except:
      logger.error("Error ao atualizar o Proprietário")

      codigo = Message(2, "Error ao atualizar o Proprietario")
      return marshal(codigo, msgFields), 400

  def delete(self, id):

    userBd = Proprietario.query.get(id)

    if userBd is None:
      logger.error(f"Proprietário de id: {id} não encontrado")

      codigo = Message(1, f"Proprietário de id: {id} não encontrado")
      return marshal(codigo, msgFields), 404

    db.session.delete(userBd)
    db.session.commit()

    logger.info(f"Proprietário de id: {id} deletado com sucesso")
    return {}, 200

class ProprietarioNome(Resource):
  def get(self, nome):
    proprietarioNome = Proprietario.query.filter(Proprietario.nome.ilike(f'%{nome}%')).all()
    logger.info(f"Proprietarios com nome: {nome} listado com sucesso")
    return marshal(proprietarioNome, userFields), 200

