from flask_restful import Resource, marshal, reqparse
from model.ingrediente import Ingrediente, ingredienteFields
from helpers.database import db
from helpers.logger import logger
from model.mensagem import Message, msgFields

parser = reqparse.RequestParser()

parser.add_argument("nome", type=str, help="Nome não informado", required=True)

class Ingredientes(Resource):
    def get(self):
      logger.info("Ingredientes listados com sucesso")
      return marshal(Ingrediente.query.all(), ingredienteFields), 200

    def post(self):
      args = parser.parse_args()
      try:
        ingrediente = Ingrediente(args['nome'])

        db.session.add(ingrediente)
        db.session.commit()

        logger.info(f"Ingrediente de id: {ingrediente.id} criado com sucesso")
        return marshal(ingrediente, ingredienteFields), 201
      except:
        logger.error("Error ao criar o ingrediente")

        codigo = Message(2, "Error ao criar o ingrediente")
        return marshal(codigo, msgFields), 400

class IngredienteId(Resource):
  def get(self, id):
    ingrediente = Ingrediente.query.get(id)

    if ingrediente is None:
      logger.error(f"Ingrediente de id: {id} não encontrado")

      codigo = Message(1, f"Ingrediente de id: {id} não encontrado")
      return marshal(codigo, msgFields), 404

    logger.info(f"Ingrediente de id: {ingrediente.id} listado com sucesso")
    return marshal(ingrediente, ingredienteFields), 200

  def put(self, id):
    args = parser.parse_args()

    try:
      ingredienteBd = Ingrediente.query.get(id)

      if ingredienteBd is None:
        logger.error(f"Ingrediente de id: {id} não encontrado")

        codigo = Message(1, f"Ingrediente de id: {id} não encontrado")
        return marshal(codigo, msgFields), 404

      ingredienteBd.nome = args["nome"]

      db.session.add(ingredienteBd)
      db.session.commit()

      logger.info(f"Ingrediente de id: {id} atualizado com sucesso")
      return marshal(ingredienteBd, ingredienteFields), 200

    except:
      logger.error("Error ao atualizar o Ingrediente")

      codigo = Message(2, "Error ao atualizar o Ingrediente")
      return marshal(codigo, msgFields), 400

  def delete(self, id):

    ingredienteBd = Ingrediente.query.get(id)

    if ingredienteBd is None:
      logger.error(f"Ingrediente de id: {id} não encontrado")

      codigo = Message(1, f"Ingrediente de id: {id} não encontrado")
      return marshal(codigo, msgFields), 404

    db.session.delete(ingredienteBd)
    db.session.commit()

    logger.info(f"Ingrediente de id: {id} deletado com sucesso")
    return {}, 200
