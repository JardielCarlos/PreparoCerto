from flask_restful import Resource, marshal, reqparse
from helpers.logger import logger
from model.utensilio import Utensilio, utensilioFields
from helpers.database import db
from model.mensagem import Message, msgError

parser = reqparse.RequestParser()

parser.add_argument("nome", type=str, help="nome nao informada", required=True)

class Utensilios(Resource):
  def get(self):
    logger.info("Utensilios Listados com sucesso")
    return marshal(Utensilio.query.all(), utensilioFields), 200
  
  def post(self):
    args = parser.parse_args()

    try:
      utensilio = Utensilio(args["nome"])

      db.session.add(utensilio)
      db.session.commit()

      logger.info(f"Utensilio de id: {utensilio.id} criado com sucesso")
      return marshal(utensilio, utensilioFields), 201
    except:
      logger.error("Error ao cadastrar Utensilio")

      codigo = Message(2, "Error ao cadastrar Utensilio")
      return marshal(codigo, msgError), 400

class UtensilioId(Resource):
  def get(self, id):
    logger.info(f"Utensilio de id: {id} listado com sucesso")

    return marshal(Utensilio.query.get(id), utensilioFields), 200
  
  def put(self, id):
    args = parser.parse_args()

    try:
      utensilioBd = Utensilio.query.get(id)

      if utensilioBd is None:
        logger.error(f"Utensilio de id: {id} nao encontrado")
        codigo = Message(1, f"Utensilio de id: {id} nao encontrado")

        return marshal(codigo, msgError), 404
      utensilioBd.nome = args["nome"]

      db.session.add(utensilioBd)
      db.session.commit()

      logger.info(f"Utensilio de id: {id} atualizado com sucesso")
      return marshal(utensilioBd, utensilioFields), 200
    except:
      logger.error("Error ao atualizar utensilio")

      codigo = Message(2, "Error ao atualizar utensilio")
      return marshal(codigo, msgError)
    
  def delete(self, id):
    utensilioBd = Utensilio.query.get(id)

    if utensilioBd is None:
      logger.info(f"Utensilio de id: {id} nao encontrado")

      codigo = Message(1, f"Utensilio de id: {id} nao encontrado")
      return marshal(codigo, msgError)

    db.session.delete(utensilioBd)
    db.session.commit()
    
    logger.info(f"Utensilio de id: {id} deletado com sucesso")
    return {}, 200
