from flask_restful import Resource, marshal, reqparse
from model.preparacao import Preparacao, preparacaoFields
from helpers.database import db
from helpers.logger import logger
from model.mensagem import Message, msgError
from model.empresa import Empresa

parser = reqparse.RequestParser()

parser.add_argument("nome", type=str, help="Nome nao informado", required=True)
parser.add_argument("componente", type=str, help="Componente nao informado", required=True)
parser.add_argument("medidaPorcao", type=str, help="medidaPorcao nao informado", required=True)
parser.add_argument("tempoPreparo", type=int, help="tempoPreparo nao informado", required=True)
parser.add_argument("rendimento", type=float, help="rendimento nao informado", required=True)
parser.add_argument("numPorcao", type=float, help="numPorcao nao informado", required=True)
parser.add_argument("indicadorConversao", type=float, help="indicadorConversao nao informado", required=True)
parser.add_argument("fatorCorrecaoGlobal", type=float, help="fatorCorrecaoGlobal nao informado", required=True)
parser.add_argument("custoPreparo", type=float, help="custoPreparo nao informado", required=True)

parser.add_argument("empresa", type=dict, help="empresa nao informado", required=False)

class Preparacoes(Resource):
  def get(self):
    logger.info("Preparacoes listadas com sucesso")
    return marshal(Preparacao.query.all(), preparacaoFields), 200
  
  def post(self):
    args = parser.parse_args()

    empresaId = args["empresa"]["id"]

    empresa = Empresa.query.get(empresaId)

    if empresa is None:
      codigo = Message(1, f"Empresa de id: {empresaId} não encontrado")
      return marshal(codigo, msgError), 404
    
    preparacao = Preparacao(args['nome'],args['componente'], args["medidaPorcao"], args['tempoPreparo'], args['rendimento'], args['numPorcao'], args['indicadorConversao'], args['fatorCorrecaoGlobal'], args['custoPreparo'], empresa)

    db.session.add(preparacao)
    db.session.commit()

    logger.info(f"Preparacao de id: {preparacao.id} criada com sucesso")
    return marshal(preparacao, preparacaoFields), 201
    
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
      preparacaoBd.componente = args['componente']
      preparacaoBd.medidaPorcao = args['medidaPorcao']
      preparacaoBd.tempoPreparo = args['tempoPreparo']
      preparacaoBd.rendimento = args['rendimento']
      preparacaoBd.numPorcao = args['numPorcao']
      preparacaoBd.indicadorConversao = args['indicadorConversao']
      preparacaoBd.fatorCorrecaoGlobal = args['fatorCorrecaoGlobal']
      preparacaoBd.custoPreparo = args['custoPreparo']

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