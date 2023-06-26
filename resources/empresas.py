from flask_restful import Resource, marshal, reqparse
from model.empresa import Empresa, empresaFieldsToken
from model.proprietario import Proprietario
from helpers.database import db
from helpers.logger import logger
from model.mensagem import Message, msgFields
from helpers.auth.token_verifier import token_verify
from sqlalchemy.exc import IntegrityError

parser = reqparse.RequestParser()

parser.add_argument("nome", type=str, help="Nome não informado", required=True)
parser.add_argument("cnpj", type=str, help="CNPJ não informado", required=True)
parser.add_argument("proprietario", type=dict, help="Proprietário não informado", required=False)


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
          logger.error(
              f"Proprietário de id: {proprietarioId} não encontrado")

          codigo = Message(
              1, f"Proprietário de id: {proprietarioId} não encontrado")
          return marshal(codigo, msgFields), 404

      empresa = Empresa(args['nome'], args["cnpj"], proprietario)

      db.session.add(empresa)
      db.session.commit()

      logger.info(f"Empresa de id: {empresa.id} criada com sucesso")
      data = {'empresa': empresa, 'token': None}

      return marshal(data, empresaFieldsToken), 201
    except IntegrityError:
      codigo = Message(1, "CNPJ ja cadastrado no sistema")
      return marshal(codigo, msgFields)

    except:
      logger.error("Error ao cadastrar a Empresa")

      codigo = Message(2, "Error ao cadastrar a empresa, verifique os campos")
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
