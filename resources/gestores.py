from flask_restful import Resource, reqparse, marshal
from helpers.database import db
from model.gestor import Gestor, gestorFields
from helpers.logger import logger
from model.mensagem import Message, msgFields
from model.empresa import Empresa
from sqlalchemy.exc import IntegrityError
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

class Gestores(Resource):
  def get(self):
    gestores = Gestor.query.all()

    logger.info("Gestores listados com sucesso")
    return marshal(gestores, gestorFields), 200

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

      empresa= Empresa.query.get(args['empresa']['id'])

      if empresa is None:
        logger.error("Empresa não encontrada")

        codigo = Message(1, 'Empresa não encontrada')
        return marshal(codigo, msgFields), 404

      gestor = Gestor(args['nome'], args["email"], args['senha'], empresa)

      db.session.add(gestor)
      db.session.commit()

      logger.info(f"Gestor de id: {gestor.id} criado com sucesso")
      return marshal(gestor, gestorFields), 201

    except TypeError:
      codigo = Message(1, "Empresa não informada")
      return marshal(codigo, msgFields), 400

    except IntegrityError:
      codigo = Message(1, "Email ja cadastrado no sistema")
      return marshal(codigo, msgFields), 400

    except:
      logger.error("Error ao cadastrar o Gestor")

      codigo = Message(2, "Error ao cadastrar o Gestor")
      return marshal(codigo, msgFields), 400

class GestorId(Resource):
  def get(self, id):
    gestor = Gestor.query.get(id)

    if gestor is None:
      logger.error(f"Gestor de id: {id} não encontrado")

      codigo = Message(1, f"Gestor de id: {id} não encontrado")
      return marshal(codigo, msgFields), 404

    logger.info(f"Gestor de id: {gestor.id} listado com sucesso")
    return marshal(gestor, gestorFields), 200

  def put(self, id):
    args = parser.parse_args()

    try:
      userBd = Gestor.query.get(id)

      if userBd is None:
        logger.error(f"Gestor de id: {id} não encontrado")

        codigo = Message(1, f"Gestor de id: {id} não encontrado")
        return marshal(codigo, msgFields), 404

      if re.match(padrao_email, args['email']) == None:
        codigo = Message(1, "Email no formato errado")
        return marshal(codigo, msgFields), 400

      verifySenha = policy.test(args['senha'])
      if len(verifySenha) != 0:
        codigo = Message(1, "Senha no formato errado")
        return marshal(codigo, msgFields), 400

      userBd.nome = args["nome"]
      userBd.email = args["email"]
      userBd.senha = args["senha"]

      db.session.add(userBd)
      db.session.commit()

      logger.info(f"Gestor de id: {id} atualizado com sucesso")
      return marshal(userBd, gestorFields), 200

    except:
      logger.error("Error ao atualizar o Gestor")

      codigo = Message(2, "Error ao atualizar o Gestor")
      return marshal(codigo, msgFields), 400

  def delete(self, id):

    userBd = Gestor.query.get(id)

    if userBd is None:
      logger.error(f"Gestor de id: {id} não encontrado")

      codigo = Message(1, f"Gestor de id: {id} não encontrado")
      return marshal(codigo, msgFields), 404

    db.session.delete(userBd)
    db.session.commit()

    logger.info(f"Gestor de id: {id} deletado com sucesso")
    return {}, 200
