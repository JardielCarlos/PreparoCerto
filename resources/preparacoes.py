from flask import make_response
from flask_restful import Resource, marshal, reqparse, request
from helpers.database import db
from helpers.logger import logger
from werkzeug.datastructures import FileStorage
from io import BytesIO
from PIL import Image

from model.mensagem import Message,msgFields
from model.preparacao import Preparacao, preparacaoFields
from model.empresa import Empresa
from model.imagem import Imagem
from model.imgPreparacao import ImgPreparacao

parser = reqparse.RequestParser()

parser.add_argument("nome", type=str, help="Nome não informado", required=True)
parser.add_argument("empresa", type=dict, help="Empresa não informada", required=False)
parser.add_argument("numPorcoes", type=float, help="Numero de porções não informado", required=True)
parser.add_argument("imagem",type=dict,help="Imagem não infotmada",required=False)

class Preparacoes(Resource):
  def get(self):
    logger.info("Preparações listadas com sucesso")
    return marshal(Preparacao.query.order_by(Preparacao.criacao).all(), preparacaoFields), 200

  def post(self):
    args = parser.parse_args()
    try:
      empresaId = args["empresa"]["id"]
      
      imagemId = args["imagem"]["id"]

      empresa = Empresa.query.get(empresaId)
      
      imagem = Imagem.query.get(imagemId)
      
      if empresa is None:
          codigo = Message(1, f"Empresa de id: {empresaId} não encontrado")
          return marshal(codigo, msgFields), 404 

      preparacao = Preparacao(args['nome'], args['numPorcoes'], empresa,imagem)

      db.session.add(preparacao)
      db.session.commit()

      imgPreparacao = ImgPreparacao(imagem, preparacao)

      db.session.add(imgPreparacao)
      db.session.commit()

      logger.info(f"Preparacao de id: {preparacao.id} criada com sucesso")
      return marshal(preparacao, preparacaoFields), 201
    except:
      logger.error("Error ao cadastrar preparacao")

      codigo = Message(2, "Error ao cadastrar preparacao")
      return marshal(codigo, msgFields), 400

class PreparacaoId(Resource):
  def get(self, id):
    preparacao = Preparacao.query.get(id)

    if preparacao is None:
      logger.error(f"Preparação de id: {id} não encontrada")

      codigo = Message(1, f"Preparação de id: {id} não encontrada")
      return marshal(codigo, msgFields), 404

    logger.info(f"Preparacao de id: {id} listada com sucesso")
    return marshal(preparacao, preparacaoFields), 200

  def put(self, id):
    args = parser.parse_args()

    try:
      preparacaoBd = Preparacao.query.get(id)
      if preparacaoBd is None:
        logger.error(f"Preparação de id: {id} não encontrada")

        codigo = Message(1, f"Preparação de id: {id} não encontrada")
        return marshal(codigo, msgFields), 404

      preparacaoBd.nome = args['nome']
      preparacaoBd.numPorcoes = args['numPorcoes']

      db.session.add(preparacaoBd)
      db.session.commit()

      logger.info(f"Preparação de id: {id} atualizada com sucesso")
      return marshal(preparacaoBd, preparacaoFields)
    except:
      logger.error("Erro ao atualizar a Preparação")

      codigo = Message(2, "Erro ao atualizar a Preparação")
      return marshal(codigo, msgFields), 400

  def delete(self, id):
    preparacaoBd = Preparacao.query.get(id)
    if preparacaoBd is None:
      logger.error(f"Preparação de id: {id} não encontrada")

      codigo = Message(1, f"Preparação de id: {id} não encontrada")
      return marshal(codigo, msgFields), 404

    db.session.delete(preparacaoBd)
    db.session.commit()

    logger.info(f"Preparacao de id: {id} deletada com sucesso")
    return {}, 200

class preparacaoImage(Resource):
  def get(self, id):
    img_io = BytesIO()

    foto = ImgPreparacao.query.filter_by(preparacao_id=id).first()
    if foto is None:
      logger.error(f"Preparacao de id: {id} nao encontrada")
      codigo = Message(1, f"Preparacao de id: {id} nao encontrada")
      return marshal(codigo, msgFields), 404

    if foto.fotoPerfil is None: return None, 200

    fotoPerfil = Image.open(BytesIO(foto.fotoPerfil))
    fotoPerfil.save(img_io, 'PNG')
    img_io.seek(0)
    response = make_response(img_io.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

  def put(self, id):
    args = parser.parse_args()

    try:
      fotoDB = ImgPreparacao.query.filter_by(preparacao_id=id).first()
      if fotoDB is None:
        logger.error(f"preparação de id: {id} não encontrada")
        codigo = Message(1, f"preparação de id: {id} não encontrada")
        return marshal(codigo, msgFields), 404

      newFoto = args['fotoPerfil']
      if newFoto is None:
        logger.error("campo fotoPerfil nao informado")
        codigo = Message(1, "campo fotoPerfil nao informado")
        return marshal(codigo, msgFields), 404
      fotoPerfil = None
      if newFoto:
        newFoto.stream.seek(0)
        fotoPerfil = newFoto.stream.read()

      fotoDB.fotoPerfil= fotoPerfil

      logger.info("Foto da preparacao atualizada com sucesso")
      db.session.add(fotoDB)
      db.session.commit()
      return {}, 204
    except:
      logger.error("Erro ao atualizar a imagem da Preparação")

      codigo = Message(2, "Erro ao atualizar a imagem da Preparação")
      return marshal(codigo, msgFields), 400

  def delete(self, id):
    foto = ImgPreparacao.query.filter_by(preparacao_id=id).first()

    if foto is None:
      logger.error(f"Imagem da preparação de id: {id} não encontrada")
      codigo = Message(1, f"Imagem da preparação de id: {id} não encontrada")
      return marshal(codigo, msgFields), 404

    foto.fotoPerfil= None

    db.session.add(foto)
    db.session.commit()

    return {}, 200
