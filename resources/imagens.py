from flask_restful import Resource, reqparse, marshal
from helpers.database import db
from model.imagem import Imagem, imagemFields
from helpers.logger import logger
from model.mensagem import Message, msgFields

parser = reqparse.RequestParser()

parser.add_argument("imagem", type=str, help="Imagem não informado", required=True)



class Imagens(Resource):
  def get(self):
    imagens = Imagem.query.all()

    if imagens == []:
      logger.error("Não existe nenhuma imagem cadastrado")
      codigo = Message(1, "Não existe nenhuma imagem cadastrado")

      return marshal(codigo, msgFields), 404
    logger.info("Imagens listadas com sucesso")
    return marshal(imagens, imagemFields), 200

  def post(self):
    args = parser.parse_args()

    try:
      if len(args['imagem']) == '':
        logger.info("Imagem nao informada")

        codigo = Message(1, "Imagem nao informada")
        return marshal(codigo, msgFields), 400


      imagem = Imagem(args['imagem'].encode())

      db.session.add(imagem)
      db.session.commit()

      logger.info(f"Imagem de id: {imagem.id} criada com sucesso")
      return marshal(imagem, imagemFields), 201
    except:
      logger.error("Error ao cadastrar a Imagem")

      codigo = Message(2, "Error ao cadastrar a Imagem")
      return marshal(codigo, msgFields), 400

class ImagemId(Resource):
  def get(self, id):
    imagem = Imagem.query.get(id)

    if imagem is None:
      logger.error(f"Imagem de id: {id} não encontrada")

      codigo = Message(1, f"Imagem de id: {id} não encontrada")
      return marshal(codigo, msgFields), 404

    logger.info(f"Imagem de id: {imagem.id} listada com Sucesso")
    return marshal(imagem, imagemFields), 200

  def put(self, id):
    args = parser.parse_args()

    try:
      imagemBd = Imagem.query.get(id)
      if imagemBd is None:
        logger.error(f"Imagem de id: {id} não encontrada")

        codigo = Message(1, f"Imagem de id: {id} não encontrada")
        return marshal(codigo, msgFields), 404

      if len(args['imagem']) == 0:
        logger.info("Imagem nao informada")

        codigo = Message(1, "Imagem nao informada")
        return marshal(codigo, msgFields), 400


      imagemBd.imagem = args["imagem"].enconde()

      db.session.add(imagemBd)
      db.session.commit()

      logger.info(f"Imagem de id: {id} atualizada com Sucesso")
      return marshal(imagemBd, imagemFields), 200

    except:
      logger.error("Error ao atualizar a Imagem")

      codigo = Message(2, "Error ao atualizar a Imagem")
      return marshal(codigo, msgFields), 400

  def delete(self, id):

    imagemBd = Imagem.query.get(id)

    if imagemBd is None:
      logger.error(f"Imagem de id: {id} não encontrada")

      codigo = Message(1, f"Imagem de id: {id} não encontrada")
      return marshal(codigo, msgFields), 404

    db.session.delete(imagemBd)
    db.session.commit()

    logger.info(f"Imagem de id: {id} deletada com sucesso")
    return {}, 200
