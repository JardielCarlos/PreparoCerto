from flask_restful import Resource, marshal, reqparse
from model.ingrediente import Ingrediente, ingredienteFields
from helpers.database import db
from helpers.logger import logger
from model.mensagem import Message, msgError

parser = reqparse.RequestParser()

parser.add_argument("nome", type=str, help="Nome nao informado", required=True)
parser.add_argument("pesoBruto", type=float, help="pesoBruto nao informado", required=True)
parser.add_argument("unidade", type=str, help="unidade nao informado", required=True)
parser.add_argument("indicadorParteComestivel", type=float, help="indicadorParteComestivel nao informado", required=True)
parser.add_argument("pesoLiquido", type=float, help="pesoLiquido nao informado", required=True)
parser.add_argument("perCapita", type=float, help="perCapita nao informado", required=True)
parser.add_argument("embalagem", type=float, help="embalagem nao informado", required=True)
parser.add_argument("preco", type=float, help="preco nao informado", required=True)
parser.add_argument("custoPreparacao", type=float, help="custoPreparacao nao informado", required=True)

class Ingredientes(Resource):
    def get(self):
      logger.info("Ingredientes listados com Sucesso")
      return marshal(Ingrediente.query.all(), ingredienteFields), 200
    
    def post(self):
      args = parser.parse_args()
      try:
        ingrediente = Ingrediente(args['nome'], args["pesoBruto"], args['unidade'], args['indicadorParteComestivel'], args['pesoLiquido'], args['perCapita'], args['embalagem'], args['preco'], args['custoPreparacao'])

        db.session.add(ingrediente)
        db.session.commit()

        logger.info(f"Ingrediente de id: {ingrediente.id} criado com sucesso")
        return marshal(ingrediente, ingredienteFields), 201
      except:
        logger.error("Error ao criar o ingrediente")

        codigo = Message(2, "Error ao criar o ingrediente")
        return marshal(codigo, msgError), 400
      
class IngredienteId(Resource):
  def get(self, id):
    ingrediente = Ingrediente.query.get(id)

    if ingrediente is None:
      logger.error(f"Ingrediente de id: {id} nao encontrado")

      codigo = Message(1, f"Ingrediente de id: {id} nao encontrado")
      return marshal(codigo, msgError), 404
    
    logger.info(f"Ingrediente de id: {ingrediente.id} Listado com Sucesso")
    return marshal(ingrediente, ingredienteFields), 200
  
  def put(self, id):
    args = parser.parse_args()

    try:
      ingredienteBd = Ingrediente.query.get(id)

      if ingredienteBd is None:
        logger.error(f"Ingrediente de id: {id} nao encontrado")

        codigo = Message(1, f"Ingrediente de id: {id} nao encontrado")
        return marshal(codigo, msgError), 404
      
      ingredienteBd.nome = args["nome"]
      ingredienteBd.pesoBruto = args["pesoBruto"]
      ingredienteBd.unidade = args["unidade"]
      ingredienteBd.indicadorParteComestivel = args["indicadorParteComestivel"]
      ingredienteBd.pesoLiquido = args["pesoLiquido"]
      ingredienteBd.perCapita = args["perCapita"]
      ingredienteBd.embalagem = args["embalagem"]
      ingredienteBd.preco = args["preco"]
      ingredienteBd.custoPreparacao = args["custoPreparacao"]
      

      db.session.add(ingredienteBd)
      db.session.commit()

      logger.info(f"Ingrediente de id: {id} atualizado com Sucesso")
      return marshal(ingredienteBd, ingredienteFields), 200
    
    except:
      logger.error("Error ao atualizar o Ingrediente")

      codigo = Message(2, "Error ao atualizar o Ingrediente")
      return marshal(codigo, msgError), 400
    
  def delete(self, id):

    ingredienteBd = Ingrediente.query.get(id)

    if ingredienteBd is None:
      logger.error(f"Ingrediente de id: {id} nao encontrado")

      codigo = Message(1, f"Ingrediente de id: {id} nao encontrado")
      return marshal(codigo, msgError), 404
    
    db.session.delete(ingredienteBd)
    db.session.commit()

    logger.info(f"Ingrediente de id: {id} deletado com sucesso")
    return {}, 200