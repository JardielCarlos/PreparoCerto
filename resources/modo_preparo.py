from flask_restful import Resource, reqparse, marshal
from helpers.database import db
from helpers.logger import logger
from model.mensagem import Message, msgError
from model.preparacao import Preparacao
from model.modo_preparo import ModoPreparo, modoPreparoFields

parser = reqparse.RequestParser()

parser.add_argument("text", type=str, help="text nao informada", required=True)
parser.add_argument("preparacao", type=dict, help="preparacao nao informada", required=True)

class ModosPreparo(Resource):

    def get(self):
      logger.info("ModosPreparo listados com sucesso")

      return marshal(ModoPreparo.query.filter_by(is_deleted=False).all(), modoPreparoFields), 200
    
    def post(self):
        args = parser.parse_args()
        try:
          preparacaoId = args["preparacao"]["id"]

          preparacao = Preparacao.query.get(preparacaoId)
          if preparacao is None:
              codigo = Message(1, f"preparacao de id: {preparacao} não encontrado")
              return marshal(codigo, msgError), 404

          modoPreparo = ModoPreparo(args['text'], preparacao)

          db.session.add(modoPreparo)
          db.session.commit()

          logger.info(f"Medida Caseira de id: {modoPreparo.id} criado com sucesso")
          return marshal(modoPreparo, modoPreparoFields), 201
        except KeyError:
            logger.error("Id da empresa não informado")
            codigo = Message(1, f"Id da empresa não informado")
            return marshal(codigo, msgError), 400
        except:
            logger.error("Error ao cadastrar Modo de preparo")

            codigo = Message(2, "Error ao cadastrar Modo de preparo")
            return marshal(codigo, msgError), 400

class ModosPreparoId(Resource):

  def get(self, preparacao_id):
     
    modopreparo = ModoPreparo.query.filter_by(preparacao_id=preparacao_id, is_deleted=False).order_by(criacao)

    if modopreparo is None:
      logger.error(f"Preparacao de id: {id} nao encontrada")

      codigo = Message(1, f"Preparacao de id: {id} nao encontrada")
      return marshal(codigo, msgError), 404

    logger.info(f"Preparacao de id: {id} listada com sucesso")
    return marshal(modopreparo, modoPreparoFields), 200

  def put(self, id):
    args = parser.parse_args()

    try:
      modoPreparoBd = ModoPreparo.query.filter_by(id=id, is_deleted=False)

      if modoPreparoBd is None:
        logger.error(f"Modo de preparo de id: {id} nao encontrado")

        codigo = Message(1, f"Modo de preparo de id: {id} nao encontrado")
        return marshal(codigo, msgError), 404

      modoPreparoBd.text = args["text"]

      db.session.add(modoPreparoBd)
      db.session.commit()

      logger.info(f"Modo de preparo de id: {id} atualizado com sucesso")
      return marshal(modoPreparoBd, modoPreparoFields), 200
    except:
      logger.error("Erro ao atualizar Modo de preparo")
      codigo = Message(2, "Erro ao atualizar Modo de preparo")
      return marshal(codigo, msgError)

  def delete(self, id):
    modoPreparoBd = ModoPreparo.query.filter_by(id=id, is_deleted=False).first()

    if modoPreparoBd is None:
        logger.error(f"Modo de preparo de id: {id} nao encontrado")
        codigo = Message(1, f"Modo de preparo de id: {id} nao encontrado")
        return marshal(codigo, msgError), 404

    modoPreparoBd.is_deleted = True
    db.session.add(modoPreparoBd)
    db.session.commit()

    logger.info(f"Modo de preparo de id: {id} deletado com sucesso")
    return {}, 200
