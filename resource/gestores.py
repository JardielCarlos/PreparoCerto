from flask_restful import Resource, reqparse, marshal
from helpers.database import db
from model.gestor import Gestor, gestorFields
from helpers.logger import logger
from model.mensagem import Message, msgError
from model.empresa import Empresa
from sqlalchemy.exc import IntegrityError
from password_strength import PasswordPolicy
import re


parser = reqparse.RequestParser()

parser.add_argument("nome", type=str, help="Nome nao informado", required=True)
parser.add_argument("email", type=str, help="email nao informado", required=True)
parser.add_argument("senha", type=str, help="senha nao informada", required=True)
parser.add_argument("empresa", type=dict, help="Empresa nao informada", required=False)

class Gestores(Resource):
  def get(self):
    logger.info("Gestores listados com Sucesso")
    return marshal(Gestor.query.all(), gestorFields), 200
  
  def post(self):
    args = parser.parse_args()

    padrao_email = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    policy = PasswordPolicy.from_names(
      length =8
    )

    try:
      
      empresa= Empresa.query.get(args['empresa']['id'])
      if empresa is None:
        logger.error("Empresa nao encontrada")

        codigo = Message(1, 'empresa não encontrada')
        return marshal(codigo, msgError), 404
      
      if re.match(padrao_email, args['email']) == None:
        codigo = Message(1, "email no formato errado")
        return marshal(codigo, msgError), 400

      verifySenha = policy.test(args['senha'])
      if len(verifySenha) != 0:
        codigo = Message(1, "senha no formato errado")
        return marshal(codigo, msgError), 400
      
      gestor = Gestor(args['nome'], args["email"], args['senha'], empresa)

      db.session.add(gestor)
      db.session.commit()

      logger.info(f"Gestor de id: {gestor.id} criado com sucesso")
      return marshal(gestor, gestorFields), 201
    
    except TypeError:
      codigo = Message(1, "Empresa nao informada")
      return marshal(codigo, msgError), 400
    
    except IntegrityError:
      codigo = Message(1, "Email ja cadastrado no sistema")
      return marshal(codigo, msgError), 400
    
    except:
      logger.error("Error ao cadastrar o Gestor")

      codigo = Message(2, "Error ao cadastrar o Gestor")
      return marshal(codigo, msgError), 400
  
class GestorId(Resource):
  def get(self, id):
    gestor = Gestor.query.get(id)

    if gestor is None:
      logger.error(f"Gestor de id: {id} nao encontrado")

      codigo = Message(1, f"Gestor de id: {id} nao encontrado")
      return marshal(codigo, msgError), 404
    
    logger.info(f"Gestor de id: {gestor.id} Listado com Sucesso")
    return marshal(gestor, gestorFields), 200
  
  def put(self, id):
    args = parser.parse_args()

    padrao_email = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    policy = PasswordPolicy.from_names(
      length =8
    )

    try:
      userBd = Gestor.query.get(id)

      if userBd is None:
        logger.error(f"Gestor de id: {id} nao encontrado")

        codigo = Message(1, f"Gestor de id: {id} nao encontrado")
        return marshal(codigo, msgError), 404
      
      if re.match(padrao_email, args['email']) == None:
        codigo = Message(1, "email no formato errado")
        return marshal(codigo, msgError), 400

      verifySenha = policy.test(args['senha'])
      if len(verifySenha) != 0:
        codigo = Message(1, "senha no formato errado")
        return marshal(codigo, msgError), 400
      
      userBd.nome = args["nome"]
      userBd.email = args["email"]
      userBd.senha = args["senha"]

      db.session.add(userBd)
      db.session.commit()
      
      logger.info(f"Gestor de id: {id} atualizado com Sucesso")
      return marshal(userBd, gestorFields), 200
    
    except:
      logger.error("Error ao atualizar o Gestor")

      codigo = Message(2, "Error ao atualizar o Gestor")
      return marshal(codigo, msgError), 400
  
  def delete(self, id):

    userBd = Gestor.query.get(id)

    if userBd is None:
      logger.error(f"Gestor de id: {id} nao encontrado")

      codigo = Message(1, f"Gestor de id: {id} nao encontrado")
      return marshal(codigo, msgError), 404

    db.session.delete(userBd)
    db.session.commit()
    
    logger.info(f"Gestor de id: {id} deletado com sucesso")
    return {}, 200
