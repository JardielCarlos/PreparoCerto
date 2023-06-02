from flask_restful import Resource, marshal, reqparse
from model.refeicao import Refeicao, refeicaoFields
from helpers.database import db
from helpers.logger import logger
from model.mensagem import Message, msgError

parser = reqparse.RequestParser()

parser.add_argument("nome", type=str, help="Nome nao imformado", required=True)

class Refeicoes(Resource):
    def get(self):
      logger.info("Refeicoes listadas com Sucesso")
      return marshal(Refeicao.query.all(), refeicaoFields), 200
    
    def post(self):
      args = parser.parse_args() 

      refeicao = Refeicao(args["nome"])

      db.session.add(refeicao)
      db.session.commit()

      logger.info(f"Refeicao de id: {refeicao.id} criado com sucesso")
      return marshal(refeicao, refeicaoFields), 201
    
class RefeicoesId(Resource):
  def get(self, id):
    logger.info("Refeicoes listados com Sucesso")

    refeicao = Refeicao.query.get(id)

    if refeicao is None:
      logger.error(f"Refeicao de id: {id} nao encontrado")

      codigo = Message(1, f"Refeicao de id: {id} nao encontrado")
      return marshal(codigo, msgError), 404

    return marshal(refeicao, refeicaoFields), 200
  
  def put(self, id):
    args = parser.parse_args()

    refeicaoBd = Refeicao.query.get(id)
    if refeicaoBd is None:
      logger.error(f"RefeicaoBd de id: {id} nao encontrado")

      codigo = Message(1, f"RefeicaoBd de id: {id} nao encontrado")
      return marshal(codigo, msgError), 404
    
    nome = args["nome"]

    refeicaoBd.nome = nome

    db.session.add(refeicaoBd)
    db.session.commit()

    logger.info(f"Refeicao de id: {id} atualizado com Sucesso")
    return marshal(refeicaoBd, refeicaoFields), 200
  
  def delete(self, id):
    refeicaoBd = Refeicao.query.get(id)

    if refeicaoBd is None:
      logger.error(f"Refeicao de id: {id} nao encontrado")

      codigo = Message(1, f"Refeicao de id: {id} nao encontrado")
      return marshal(codigo, msgError), 404

    db.session.delete(refeicaoBd)
    db.session.commit()
    
    logger.info(f"Refeicao de id: {id} deletado com sucesso")
    return {}, 200
