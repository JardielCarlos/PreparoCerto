from flask import Flask
from flask_restful import Api
from helpers.database import db, migrate
from helpers.configCORS import cors

from resources.preparadores import Preparadores, PreparadorId
from resources.gestores import Gestores, GestorId
from resources.ingredientes import Ingredientes, IngredienteId
from resources.empresas import Empresas, EmpresaId
from resources.proprietarios import Proprietarios, ProprietarioId
from resources.preparacoes import Preparacoes, PreparacaoId
from resources.cardapios import Cardapios, CardapioId
from resources.preparacao_ingrediente import PreparacaoIngredientes, PreparacaoIngredientesId
from resources.cardapio_preparacao import CardapioPreapracoes, CardapioPreapracaoId
from resources.ficha_tecnica import FichaTecnicaOperacional, FichaTecnicaGerencial
from resources.unidade import Unidade, UnidadeId
from resources.medida_caseira import MedidasCaseiras, MedidaCaseiraId
from resources.utensilios import Utensilios, UtensilioId
from resources.preparacao_utensilio import UtensiliosPreparacao, UtensiliosPreparacaoId
from resources.login import Login
from resources.logout import Logout
from resources.modo_preparo import ModosPreparo, ModosPreparoId
from resources.usuario import Usuarios

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://postgres:senha@localhost:5432/PreparoCerto"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
cors.init_app(app)
migrate.__init__(app, db)
api = Api(app)

#Gestor
api.add_resource(Gestores, '/gestor')
api.add_resource(GestorId, '/gestor/<int:id>')

#Preparador
api.add_resource(Preparadores, '/preparadores')
api.add_resource(PreparadorId, '/preparadores/<int:id>')

#Ingrediente
api.add_resource(Ingredientes, '/ingredientes')
api.add_resource(IngredienteId, '/ingrediente/<int:id>')

#Empresa
api.add_resource(Empresas, '/empresas')
api.add_resource(EmpresaId, '/empresas/<int:id>')

#Proprietario
api.add_resource(Proprietarios, '/proprietarios')
api.add_resource(ProprietarioId, '/proprietario/<int:id>')

#Preparacao
api.add_resource(Preparacoes, '/preparacoes')
api.add_resource(PreparacaoId, '/preparacao/<int:id>')

#Cardapio
api.add_resource(Cardapios, '/cardapios')
api.add_resource(CardapioId, '/cardapio/<int:id>')

#Preparacao_Ingrediente
api.add_resource(PreparacaoIngredientes, '/preparacao_ingrediente')
api.add_resource(PreparacaoIngredientesId, '/preparacao_ingrediente/<int:id>')

#Cardapio_Preparacao
api.add_resource(CardapioPreapracoes, '/cardapio_preparacao')
api.add_resource(CardapioPreapracaoId, '/cardapio_preparacao/<int:id>')

#Ficha Tecnica Operacional
api.add_resource(FichaTecnicaOperacional, '/fichatecnicaoperacional/<int:id>')

#Ficha Tecnica Gerencial
api.add_resource(FichaTecnicaGerencial, '/fichatecnicagerencial/<int:id>')

#Unidade Medida
api.add_resource(Unidade, '/unidade')
api.add_resource(UnidadeId, '/unidade/<int:id>')

#Medida Caseira
api.add_resource(MedidasCaseiras, '/medidas')
api.add_resource(MedidaCaseiraId, '/medidas/<int:id>')

#Utensilio
api.add_resource(Utensilios, '/utensilios')
api.add_resource(UtensilioId, '/utensilio/<int:id>')

#Login
api.add_resource(Login, '/login')

#Logout
api.add_resource(Logout, '/logout')

#ModoPreparo
api.add_resource(ModosPreparo, '/modospreparo')
api.add_resource(ModosPreparoId, '/modospreparo/<int:id>')

#Usuario
api.add_resource(Usuarios, '/usuarios')

#UtensiliosPreparacao
api.add_resource(UtensiliosPreparacao, '/utensilios_preparacao')
api.add_resource(UtensiliosPreparacaoId, '/utensilios_preparacao/<int:id>')

if __name__ == '__main__':
  app.run(debug=True)
