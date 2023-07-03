from flask_restful import Resource, marshal, reqparse
from helpers.database import db
from helpers.logger import logger
from sqlalchemy.exc import IntegrityError
from helpers.auth.token_verifier import token_verify

from model.ingrediente import Ingrediente, ingredienteTokenFields
from model.mensagem import Message, msgFields

parser = reqparse.RequestParser()

parser.add_argument("nome", type=str, help="Nome não informado", required=True)
parser.add_argument("codigo", type=str, help="codigo não informado", required=True)

class Ingredientes(Resource):
  @token_verify
  def post(self, tipo, refreshToken):
    if tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar os ingredientes")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

    args = parser.parse_args()
    try:
      ingrediente = Ingrediente(args['codigo'], args['nome'])

      db.session.add(ingrediente)
      db.session.commit()

      data = {'ingrediente': ingrediente, 'token': refreshToken}

      logger.info(f"Ingrediente de id: {ingrediente.id} criado com sucesso")
      return marshal(data, ingredienteTokenFields), 201
    except:
      logger.error("Error ao criar o ingrediente")

      codigo = Message(2, "Error ao criar o ingrediente")
      return marshal(codigo, msgFields), 400

class IngredienteId(Resource):
  @token_verify
  def get(self, tipo, refreshToken, id):
    if tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar os ingredientes")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

    ingrediente = Ingrediente.query.get(id)

    if ingrediente is None:
      logger.error(f"Ingrediente de id: {id} não encontrado")

      codigo = Message(1, f"Ingrediente de id: {id} não encontrado")
      return marshal(codigo, msgFields), 404

    data = {'ingrediente': ingrediente, 'token': refreshToken}


    logger.info(f"Ingrediente de id: {ingrediente.id} listado com sucesso")
    return marshal(data, ingredienteTokenFields), 200

  @token_verify
  def put(self, tipo, refreshToken, id):
    if tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar os ingredientes")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

    args = parser.parse_args()

    try:
      ingredienteBd = Ingrediente.query.get(id)

      if ingredienteBd is None:
        logger.error(f"Ingrediente de id: {id} não encontrado")

        codigo = Message(1, f"Ingrediente de id: {id} não encontrado")
        return marshal(codigo, msgFields), 404

      ingredienteBd.codigo = args['codigo']
      ingredienteBd.nome = args["nome"]

      db.session.add(ingredienteBd)
      db.session.commit()

      data = {'ingrediente': ingredienteBd, 'token': refreshToken}


      logger.info(f"Ingrediente de id: {id} atualizado com sucesso")
      return marshal(data, ingredienteTokenFields), 200

    except:
      logger.error("Error ao atualizar o Ingrediente")

      codigo = Message(2, "Error ao atualizar o Ingrediente")
      return marshal(codigo, msgFields), 400

  @token_verify
  def delete(self, tipo, refreshToken, id):
    if tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar os ingredientes")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403
    try:
      ingredienteBd = Ingrediente.query.get(id)

      if ingredienteBd is None:
        logger.error(f"Ingrediente de id: {id} não encontrado")

        codigo = Message(1, f"Ingrediente de id: {id} não encontrado")
        return marshal(codigo, msgFields), 404

      db.session.delete(ingredienteBd)
      db.session.commit()

      logger.info(f"Ingrediente de id: {id} deletado com sucesso")
      return {'token': refreshToken}, 200
    except IntegrityError:
      logger.error(f"Ingrediente de id: {id} não pode ser deletado possui dependencia com a preparacao_ingrediente")

      codigo = Message(1, f"Ingrediente de id: {id} não pode ser deletado possui dependencia com a preparacao do ingrediente")
      return marshal(codigo, msgFields), 400

class IngredienteNome(Resource):
  @token_verify
  def get(self, tipo, refreshToken, nome):
    if tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar os ingredientes")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

    IngredienteNome = Ingrediente.query.filter(Ingrediente.nome.ilike(f'%{nome}%')).all()

    data = {'ingrediente': IngredienteNome, 'token': refreshToken}

    logger.info(f"Ingredinte de nome: {nome} listado")
    return marshal(data, ingredienteTokenFields), 200

class IngredientePagination(Resource):
  @token_verify
  def get(self, tipo, refreshToken, id):
    if tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar os ingredientes")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

    ingredientes = Ingrediente.query.paginate(page=id, per_page=10, error_out=False)
    data = {'ingrediente': ingredientes.items, 'token': refreshToken}

    logger.info("Ingredientes listados com sucesso")
    return marshal(data, ingredienteTokenFields), 200
