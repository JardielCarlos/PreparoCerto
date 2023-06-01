from flask_restful import Resource, marshal, reqparse
from helpers.database import db
from helpers.logger import logger
from model.mensagem import Message, msgError

from model.refeicao_preparacao import RefeicaoPreparacao ,refeicaoPreparacaoFields
from model.preparacao import Preparacao
from model.refeicao import Refeicao

parser = reqparse.RequestParser()

parser.add_argument("preparacao", type=dict, help="preparacao nao informado", required=True)
parser.add_argument("refeicao", type=dict, help="refeicao nao informado", required=True)

class RefeicoesPreparacao(Resource):
  def get(self):
    logger.info("Refeicao-preparacao listados com sucesso")

    refeicaoPreparacao = RefeicaoPreparacao.query.all()

    return marshal(refeicaoPreparacao, refeicaoPreparacaoFields), 200
  
  def post(self):
    args = parser.parse_args()

    refeicaoId = args['refeicao']['id']
    preparacaoId = args['preparacao']['id']

    refeicao = Refeicao.query.get(refeicaoId)
    preparacao = Preparacao.query.get(preparacaoId)
    if refeicao is None:
      codigo = Message(1, f"Refeicao de id: {refeicaoId} não encontrado")
      return marshal(codigo, msgError), 404
    elif preparacao is None:
      codigo = Message(1, f"Preparacao de id: {preparacaoId} não encontrada")
      return marshal(codigo, msgError), 404
    
    refeicaoPreparacao = RefeicaoPreparacao(refeicao, preparacao)
    db.session.add(refeicaoPreparacao)
    db.session.commit()

    logger.info(f"PreparacaoRefeicao de id: {refeicaoPreparacao.id} criado com sucesso")
    return marshal(refeicaoPreparacao, refeicaoPreparacaoFields), 201

class RefeicoesPreparacaoId(Resource):
  def get(self, id):
    refeicaoPreparacao = RefeicaoPreparacao.query.get(id)

    if refeicaoPreparacao is None:
      logger.error(f"PreparacaoRefeicao de id: {id} nao encontrado")

      codigo = Message(1, f"PreparacaoRefeicao de id: {id} nao encontrado")
      return marshal(codigo, msgError), 404
    
    logger.info(f"PreparacaoRefeicao de id: {refeicaoPreparacao.id} Listado com Sucesso")
    return marshal(refeicaoPreparacao, refeicaoPreparacaoFields), 200
  
  def put(self, id):
    args = parser.parse_args()

    refeicaoPreparacaoBd = RefeicaoPreparacao.query.get(id)
    preparacaoId = args['preparacao']['id']
    refeicaoId = args['refeicao']['id']

    if refeicaoPreparacaoBd is None:
      logger.error(f"RefeicaoPreparacao de id: {id} nao encontrada")

      codigo = Message(1, f"RefeicaoPreparacao de id: {id} nao encontrada")
      return marshal(codigo, msgError), 404
    
    preparacao = Preparacao.query.get(preparacaoId)
    refeicao = Refeicao.query.get(refeicaoId)

    if preparacao is None:
      codigo = Message(1, f"Preparacao de id: {preparacaoId} não encontrada")
      return marshal(codigo, msgError), 404
    elif refeicao is None:
      codigo = Message(1, f"Refeicao de id: {refeicaoId} não encontrado")
      return marshal(codigo, msgError), 404
    
    refeicaoPreparacaoBd.preparacao = preparacao
    refeicaoPreparacaoBd.refeicao = refeicao

    db.session.add(refeicaoPreparacaoBd)
    db.session.commit()

    logger.info(f"RefeicaoPreparacao de id: {id} atualizada com sucesso")
    return marshal(refeicaoPreparacaoBd, refeicaoPreparacaoFields)
  
  def delete(self, id):
    refeicaoPreparacaoBd = RefeicaoPreparacao.query.get(id)

    if refeicaoPreparacaoBd is None:
      logger.error(f"RefeicaoPreparacao de id: {id} nao encontrado")

      codigo = Message(1, f"RefeicaoPreparacao de id: {id} nao encontrado")
      return marshal(codigo, msgError), 404
    
    db.session.delete(refeicaoPreparacaoBd)
    db.session.commit()

    logger.info(f"RefeicaoPreparacao de id: {id} deletado com sucesso")
    return {}, 200
    
