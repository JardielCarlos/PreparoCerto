from flask_restful import Resource, marshal, reqparse
from model.empresa import Empresa, empresaFields
from helpers.database import db
from helpers.logger import logger
from model.mensagem import Message, msgError

parser = reqparse.RequestParser()

parser.add_argument("nome", type=str, help="Nome nao informado", required=True)
parser.add_argument("cnpj", type=str, help="CNPJ nao informado", required=True)
parser.add_argument("id_gestor", type=str, help="id do gestor nao informado", required=False)

class Empresas(Resource):
  def get(self):
    logger.info("Empresas listadas com Sucesso")
    return marshal(Empresa.query.all(), empresaFields), 200
  
  def post(self):
    args = parser.parse_args()

    try:
      empresa = Empresa(args['nome'], args["cnpj"], args['id_gestor'])
      if empresa.id_gestor is None:
        logger.error("Id do gestor nao informado")

        codigo = Message(1, "Id do gestor nao informado")
        return marshal(codigo, msgError), 400

      db.session.add(empresa)
      db.session.commit()

      logger.info(f"Empresa de id: {empresa.id} criado com sucesso")
      return marshal(empresa, empresaFields), 201

    except:
      logger.error("Error ao cadastrar o Empresa")

      codigo = Message(2, "Error ao cadastrar o Empresa")
      return marshal(codigo, msgError), 400
    
class EmpresaId(Resource):
  def get(self, id):
    empresa = Empresa.query.get(id)

    if empresa is None:
      logger.error(f"Empresa de id: {id} nao encontrado")

      codigo = Message(1, f"Empresa de id: {id} nao encontrado")
      return marshal(codigo, msgError), 404
    
    logger.info(f"Empresa de id: {empresa.id} Listado com Sucesso")
    return marshal(empresa, empresaFields), 200
  
  def put(self, id):
    args = parser.parse_args()

    try:
      empresaBd = Empresa.query.get(id)

      if empresaBd is None:
        logger.error(f"Empresa de id: {id} nao encontrado")

        codigo = Message(1, f"Empresa de id: {id} nao encontrado")
        return marshal(codigo, msgError), 404
      
      empresaBd.nome = args["nome"]
      empresaBd.cnpj = args["cnpj"]

      db.session.add(empresaBd)
      db.session.commit()
      
      logger.info(f"Empresa de id: {id} atualizado com Sucesso")
      return marshal(empresaBd, empresaFields), 200
    
    except:
      logger.error("Error ao atualizar o Empresa")

      codigo = Message(2, "Error ao atualizar o Empresa")
      return marshal(codigo, msgError), 400
    
  def delete(self, id):

    empresaBd = Empresa.query.get(id)

    if empresaBd is None:
      logger.error(f"Empresa de id: {id} nao encontrado")

      codigo = Message(1, f"Empresa de id: {id} nao encontrado")
      return marshal(codigo, msgError), 404

    db.session.delete(empresaBd)
    db.session.commit()
    
    logger.info(f"Empresa de id: {id} deletado com sucesso")
    return {}, 200