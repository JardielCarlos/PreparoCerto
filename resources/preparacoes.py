from flask import make_response
from flask_restful import Resource, marshal, reqparse, request
from helpers.database import db
from helpers.auth.token_verifier import token_verify
from helpers.logger import logger
from werkzeug.datastructures import FileStorage
from io import BytesIO
from PIL import Image

from model.preparacao import Preparacao, preparacaoTokenFields
from model.empresa import Empresa
from model.imgPreparacao import ImgPreparacao
from model.mensagem import Message, msgFields

parser = reqparse.RequestParser()

parser.add_argument('fotoPerfil', type=FileStorage, location='files')

class Preparacoes(Resource):
  @token_verify
  def get(self, tipo, refreshToken):
    if tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar as preparacoes")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

    logger.info("Preparações listadas com sucesso")

    preparacoes = Preparacao.query.order_by(Preparacao.criacao).all()

    data = {'preparacao': preparacoes, 'token': refreshToken}

    return marshal(data, preparacaoTokenFields), 200

  @token_verify
  def post(self, tipo, refreshToken):
    if tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar as preparacoes")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

    args = parser.parse_args()
    try:
      empresaId = request.form['empresa']
      if not empresaId:
        logger.info("Id da empresa nao informado")

        codigo = Message(1, "Id da empresa nao informado")
        return marshal(codigo, msgFields), 400

      empresa = Empresa.query.get(empresaId)
      if empresa is None:
          codigo = Message(1, f"Empresa de id: {empresaId} não encontrado")
          return marshal(codigo, msgFields), 404

      foto = args['fotoPerfil']
      fotoPerfil = None

      if foto:
        foto.stream.seek(0)
        fotoPerfil = foto.stream.read()

      if not request.form['nome']:
        logger.info("Nome nao informado")

        codigo = Message(1, "Nome nao informado")
        return marshal(codigo, msgFields), 400

      if not request.form['numPorcoes']:
        logger.info("numeros das porcoes nao informada")

        codigo = Message(1, "numeros das porcoes nao informada")
        return marshal(codigo, msgFields), 400

      preparacao = Preparacao(request.form['nome'], request.form['numPorcoes'], empresa)

      db.session.add(preparacao)
      db.session.commit()

      imgPreparacao = ImgPreparacao(fotoPerfil, preparacao)

      db.session.add(imgPreparacao)
      db.session.commit()

      data = {'preparacao': preparacao, 'token': refreshToken}

      logger.info(f"Preparacao de id: {preparacao.id} criada com sucesso")
      return marshal(data, preparacaoTokenFields), 201
    except:
      logger.error("Error ao cadastrar preparacao")

      codigo = Message(2, "Error ao cadastrar preparacao")
      return marshal(codigo, msgFields), 400

class PreparacaoId(Resource):
  @token_verify
  def get(self, tipo, refreshToken, id):
    if tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar as preparacoes")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

    preparacao = Preparacao.query.get(id)

    if preparacao is None:
      logger.error(f"Preparação de id: {id} não encontrada")

      codigo = Message(1, f"Preparação de id: {id} não encontrada")
      return marshal(codigo, msgFields), 404

    data = {'preparacao': preparacao, 'token': refreshToken}

    logger.info(f"Preparacao de id: {id} listada com sucesso")
    return marshal(data, preparacaoTokenFields), 200

  @token_verify
  def put(self, tipo, refreshToken, id):
    if tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar as preparacoes")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

    # args = parser.parse_args()
    try:
      preparacaoBd = Preparacao.query.get(id)
      if preparacaoBd is None:
        logger.error(f"Preparação de id: {id} não encontrada")

        codigo = Message(1, f"Preparação de id: {id} não encontrada")
        return marshal(codigo, msgFields), 404

      if not request.form['nome']:
        logger.info("Nome nao informado")

        codigo = Message(1, "Nome nao informado")
        return marshal(codigo, msgFields), 400

      if not request.form['numPorcoes']:
        logger.info("numeros das porcoes nao informada")

        codigo = Message(1, "numeros das porcoes nao informada")
        return marshal(codigo, msgFields), 400

      preparacaoBd.nome = request.form['nome']
      preparacaoBd.numPorcoes = request.form['numPorcoes']

      db.session.add(preparacaoBd)
      db.session.commit()

      data = {'preparacao': preparacaoBd, 'token': refreshToken}

      logger.info(f"Preparação de id: {id} atualizada com sucesso")
      return marshal(data, preparacaoTokenFields)
    except:
      logger.error("Erro ao atualizar a Preparação")

      codigo = Message(2, "Erro ao atualizar a Preparação")
      return marshal(codigo, msgFields), 400

  @token_verify
  def delete(self, tipo, refreshToken, id):
    if tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar as preparacoes")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

    preparacaoBd = Preparacao.query.get(id)
    if preparacaoBd is None:
      logger.error(f"Preparação de id: {id} não encontrada")

      codigo = Message(1, f"Preparação de id: {id} não encontrada")
      return marshal(codigo, msgFields), 404

    db.session.delete(preparacaoBd)
    db.session.commit()

    logger.info(f"Preparacao de id: {id} deletada com sucesso")
    return {'token': refreshToken}, 200

class preparacaoImage(Resource):
  @token_verify
  def get(self, tipo, refreshToken, id):
    if tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar as imagens das preparacoes")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

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

  @token_verify
  def put(self, tipo, refreshToken, id):
    if tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar as imagens das preparacoes")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

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
  @token_verify
  def delete(self, tipo, refreshToken, id):
    if tipo != 'proprietario' and tipo != 'gestor':
      logger.error("Usuario sem autorizacao para acessar as imagens das preparacoes")

      codigo = Message(1, "Usuario sem autorização suficiente!")
      return marshal(codigo, msgFields), 403

    foto = ImgPreparacao.query.filter_by(preparacao_id=id).first()

    if foto is None:
      logger.error(f"Imagem da preparação de id: {id} não encontrada")
      codigo = Message(1, f"Imagem da preparação de id: {id} não encontrada")
      return marshal(codigo, msgFields), 404

    foto.fotoPerfil= None

    db.session.add(foto)
    db.session.commit()

    return {}, 200
