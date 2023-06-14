from flask_restful import Resource, marshal, reqparse
from model.empresa import Empresa, empresaFieldsToken
from model.proprietario import Proprietario
from helpers.database import db
from helpers.logger import logger
from model.mensagem import Message, msgError
from helpers.auth.token_verifier import token_verify
from sqlalchemy.exc import IntegrityError

parser = reqparse.RequestParser()

parser.add_argument("nome", type=str, help="Nome nao informado", required=True)
parser.add_argument("cnpj", type=str, help="CNPJ nao informado", required=True)
parser.add_argument("proprietario", type=dict,
                    help="proprietario nao informado", required=False)


class Empresas(Resource):
    @token_verify
    def get(self, tipo, token):
        if tipo != 'proprietario':
            logger.error("Usuario sem autorização suficiente!")
            codigo = Message(1, "Usuario sem autorização suficiente!")
            return marshal(codigo, msgError), 403

        empresa = Empresa.query.all()
        data = {'empresa': empresa, 'token': token}

        logger.info("Empresas listadas com Sucesso")
        return marshal(data, empresaFieldsToken), 200

    # @token_verify
    def post(self):
        args = parser.parse_args()

        # if tipo != 'proprietario':
        #     logger.error("Usuario sem autorização suficiente!")

        #     codigo = Message(1, "Usuario sem autorização suficiente!")
        #     return marshal(codigo, msgError), 403

        try:
            proprietarioId = args["proprietario"]['id']
            proprietario = Proprietario.query.get(proprietarioId)

            if proprietario is None:
                logger.error(
                    f"Proprietario de id: {proprietarioId} nao encontrado")

                codigo = Message(
                    1, f"Proprietario de id: {proprietarioId} nao encontrado")
                return marshal(codigo, msgError), 404

            empresa = Empresa(args['nome'], args["cnpj"], proprietario)

            db.session.add(empresa)
            db.session.commit()

            logger.info(f"Empresa de id: {empresa.id} criado com sucesso")
            data = {'empresa': empresa, 'token': None}

            return marshal(data, empresaFieldsToken), 201
        except IntegrityError:
            codigo = Message(1, "CNPJ ja cadastrado no sistema")
            return marshal(codigo, msgError)

        except:
            logger.error("Error ao cadastrar o Empresa")

            codigo = Message(
                2, "Error ao cadastrar a empresa verifique os campos")
            return marshal(codigo, msgError), 400


class EmpresaId(Resource):
    @token_verify
    def get(self, tipo, token, id):
        if tipo != 'proprietario':
            logger.error("Usuario sem autorização suficiente!")

            codigo = Message(1, "Usuario sem autorização suficiente!")
            return marshal(codigo, msgError), 403

        empresa = Empresa.query.get(id)
        if empresa is None:
            logger.error(f"Empresa de id: {id} nao encontrado")

            codigo = Message(1, f"Empresa de id: {id} nao encontrado")
            return marshal(codigo, msgError), 404
        data = {'empresa': empresa, 'token': token}

        logger.info(f"Empresa de id: {empresa.id} Listado com Sucesso")
        return marshal(data, empresaFieldsToken), 200

    @token_verify
    def put(self, tipo, token, id):
        args = parser.parse_args()

        if tipo != 'proprietario':
            logger.error("Usuario sem autorização suficiente!")

            codigo = Message(1, "Usuario sem autorização suficiente!")
            return marshal(codigo, msgError), 403

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
            data = {'empresa': empresaBd, 'token': token}

            logger.info(f"Empresa de id: {id} atualizado com Sucesso")
            return marshal(data, empresaFieldsToken), 200

        except:
            logger.error("Error ao atualizar o Empresa")

            codigo = Message(2, "Error ao atualizar o Empresa")
            return marshal(codigo, msgError), 400

    @token_verify
    def delete(self, tipo, token, id):
        print(id, "to aqui")
        if tipo != 'proprietario':
            logger.error("Usuario sem autorização suficiente!")

            codigo = Message(1, "Usuario sem autorização suficiente!")
            return marshal(codigo, msgError), 403

        empresaBd = Empresa.query.get(id)

        if empresaBd is None:
            logger.error(f"Empresa de id: {id} nao encontrado")

            codigo = Message(1, f"Empresa de id: {id} nao encontrado")
            return marshal(codigo, msgError), 404

        db.session.delete(empresaBd)
        db.session.commit()

        logger.info(f"Empresa de id: {id} deletado com sucesso")
        return {'token': token}, 200
