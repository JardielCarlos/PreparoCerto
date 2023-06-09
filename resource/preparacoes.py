from flask_restful import Resource, marshal, reqparse
from model.preparacao import Preparacao, preparacaoFields
from helpers.database import db
from helpers.logger import logger
from model.mensagem import Message, msgError
from model.empresa import Empresa
from model.modo_preparo import ModoPreparo

parser = reqparse.RequestParser()

parser.add_argument("nome", type=str, help="Nome nao informado", required=True)
parser.add_argument("empresa", type=dict, help="empresa nao informado", required=False)
parser.add_argument("modoPreparo", type=dict, help="Modo de preparo nao informado", required=True)

class Preparacoes(Resource):
  def get(self):
    logger.info("Preparacoes listadas com sucesso")
    return marshal(Preparacao.query.all(), preparacaoFields), 200
  
  def post(self):
    args = parser.parse_args()
    try:
      empresaId = args["empresa"]["id"]
      modoPreparoId = args["modoPreparo"]["id"]

      empresa = Empresa.query.get(empresaId)
      modoPreparo = ModoPreparo.query.get(modoPreparoId)

      if empresa is None:
        codigo = Message(1, f"Empresa de id: {empresaId} não encontrado")
        return marshal(codigo, msgError), 404
      elif modoPreparo is None:
        codigo = Message(1, f"Modo de preparo de id: {modoPreparoId} não encontrado")
        return marshal(codigo, msgError), 404
      
      preparacao = Preparacao(args['nome'], empresa, modoPreparo)

      db.session.add(preparacao)
      db.session.commit()

      logger.info(f"Preparacao de id: {preparacao.id} criada com sucesso")
      return marshal(preparacao, preparacaoFields), 201
    except:
      logger.error("Error ao cadastrar preparacao")

      codigo = Message(2, "Error ao cadastrar preparacao")
      return marshal(codigo, msgError), 400
      
class PreparacaoId(Resource):
  def get(self, id):
    preparacao = Preparacao.query.get(id)

    if preparacao is None:
      logger.error(f"Preparacao de id: {id} nao encontrada")

      codigo = Message(1, f"Preparacao de id: {id} nao encontrada")
      return marshal(codigo, msgError), 404
    
    logger.info(f"Preparacao de id: {id} listada com sucesso")
    return marshal(preparacao, preparacaoFields), 200
  
  def put(self, id):
    args = parser.parse_args()

    try:
      preparacaoBd = Preparacao.query.get(id)
      if preparacaoBd is None:
        logger.error(f"Preparacao de id: {id} nao encontrada")

        codigo = Message(1, f"Preparacao de id: {id} nao encontrada")
        return marshal(codigo, msgError), 404
      
      preparacaoBd.nome = args['nome']

      db.session.add(preparacaoBd)
      db.session.commit()

      logger.info(f"Preparacao de id: {id} atualizada com sucesso")
      return marshal(preparacaoBd, preparacaoFields)
    except:
      logger.error("Erro ao atualizar a Preparacao")

      codigo = Message(2, "Erro ao atualizar a Preparacao")
      return marshal(codigo, msgError), 400
    
  def delete(self, id):
    preparacaoBd = Preparacao.query.get(id)

    if preparacaoBd is None:
      logger.error(f"Preparacao de id: {id} nao encontrada")

      codigo = Message(1, f"Preparacao de id: {id} nao encontrada")
      return marshal(codigo, msgError), 404

    db.session.delete(preparacaoBd)
    db.session.commit()

    logger.info(f"Preparacao de id: {id} deletada com sucesso")
    return {}, 200