from flask_restful import Resource, marshal, reqparse
from helpers.database import db
from helpers.logger import logger
from validate_docbr import CNPJ
import re

from helpers.auth.token_verifier import token_verify

from sqlalchemy.exc import IntegrityError

from model.mensagem import Message, msgFields
from model.proprietario import Proprietario
from model.empresa import Empresa, empresaFieldsToken

parser = reqparse.RequestParser()

parser.add_argument("nome", type=str, help="Nome não informado", required=True)
parser.add_argument("cnpj", type=str, help="CNPJ não informado", required=True)
parser.add_argument("proprietario", type=dict, help="Proprietário não informado", required=False)

cnpjValidate = CNPJ()

# Exemplos CNPJ valido{
#   "70.094.628/0001-89"
#   "77.879.004/0056-90"
#   "04.734.271/4847-30"
#   "87.321.171/6847-17"
# }

class Empresas(Resource):
  @token_verify
  def get(self, tipo, token):
    if tipo != 'proprietario':
      logger.error("Usuario sem autorização suficiente!")
      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

    empresa = Empresa.query.all()

    data = {'empresa': empresa, 'token': token}

    logger.info("Empresas listadas com Sucesso")
    return marshal(data, empresaFieldsToken), 200

  #@token_verify
  def post(self):
    args = parser.parse_args()

    #if tipo != 'proprietario':
    #  logger.error("Usuario sem autorização suficiente!")

    #  codigo = Message(1, "Usuario sem autorização suficiente!")
    #  return marshal(codigo, msgFields), 403

    try:
      proprietarioId = args["proprietario"]['id']
      proprietario = Proprietario.query.get(proprietarioId)

      if proprietario is None:
        logger.error(f"Proprietário de id: {proprietarioId} não encontrado")

        codigo = Message(1, f"Proprietário de id: {proprietarioId} não encontrado")
        return marshal(codigo, msgFields), 404

      if not cnpjValidate.validate(args["cnpj"]):
        logger.error(f"CNPJ {args['cnpj']} não valido")

        codigo = Message(1, f"CNPJ {args['cnpj']} não valido")
        return marshal(codigo, msgFields), 400

      if not re.match(r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$', args["cnpj"]):
        logger.error(f"CNPJ {args['cnpj']} no formato errado")

        codigo = Message(1, "CNPJ no formato errado")
        return marshal(codigo, msgFields), 400

      empresa = Empresa(args['nome'], args["cnpj"], proprietario)

      db.session.add(empresa)
      db.session.commit()

      logger.info(f"Empresa de id: {empresa.id} criada com sucesso")
      data = {'empresa': empresa, 'token': None}

      return marshal(data, empresaFieldsToken), 201
    except IntegrityError:
      codigo = Message(1, "CNPJ ja cadastrado no sistema")
      return marshal(codigo, msgFields), 400

    except KeyError:
      codigo = Message(1,"Id do proprietario não informado")
      return marshal(codigo, msgFields), 400

    except:
      logger.error("Error ao cadastrar a Empresa")
      codigo = Message(2, "Proprietario nao informado")
      return marshal(codigo, msgFields), 400


class EmpresaId(Resource):
  @token_verify
  def get(self, tipo, token, id):
    if tipo != 'proprietario':
      logger.error("Usuario sem autorização suficiente!")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

    empresa = Empresa.query.get(id)
    if empresa is None:
      logger.error(f"Empresa de id: {id} não encontrada")

      codigo = Message(1, f"Empresa de id: {id} não encontrada")
      return marshal(codigo, msgFields), 404
    data = {'empresa': empresa, 'token': token}

    logger.info(f"Empresa de id: {empresa.id} listada com sucesso")
    return marshal(data, empresaFieldsToken), 200

  @token_verify
  def put(self, tipo, token, id):
    args = parser.parse_args()

    if tipo != 'proprietario':
      logger.error("Usuario sem autorização suficiente!")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

    try:
      empresaBd = Empresa.query.get(id)

      if empresaBd is None:
        logger.error(f"Empresa de id: {id} não encontrada")

        codigo = Message(1, f"Empresa de id: {id} não encontrada")
        return marshal(codigo, msgFields), 404

      if not re.match(r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$', args["cnpj"]):
        codigo = Message(1, "CNPJ no formato errado")
        return marshal(codigo, msgFields), 400

      empresaBd.nome = args["nome"]
      empresaBd.cnpj = args["cnpj"]

      db.session.add(empresaBd)
      db.session.commit()
      data = {'empresa': empresaBd, 'token': token}

      logger.info(f"Empresa de id: {id} atualizada com sucesso")
      return marshal(data, empresaFieldsToken), 200

    except IntegrityError:
      codigo = Message(1, "CNPJ ja cadastrado no sistema")
      return marshal(codigo, msgFields)

    except:
      logger.error("Error ao atualizar a empresa")

      codigo = Message(2, "Error ao atualizar a empresa")
      return marshal(codigo, msgFields), 400

  @token_verify
  def delete(self, tipo, token, id):
    if tipo != 'proprietario':
      logger.error("Usuario sem autorização suficiente!")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

    empresaBd = Empresa.query.get(id)

    if empresaBd is None:
      logger.error(f"Empresa de id: {id} não encontrada")

      codigo = Message(1, f"Empresa de id: {id} não encontrada")
      return marshal(codigo, msgFields), 404

    db.session.delete(empresaBd)
    db.session.commit()

    logger.info(f"Empresa de id: {id} deletada com sucesso")
    return {'token': token}, 200
