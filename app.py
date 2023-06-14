from flask import Flask
from flask_restful import Api
from helpers.database import db, migrate

from resource.preparadores import Preparadores, PreparadorId
from resource.gestores import Gestores, GestorId
from resource.ingredientes import Ingredientes, IngredienteId
from resource.empresas import Empresas, EmpresaId
from resource.proprietarios import Proprietarios, ProprietarioId
from resource.preparacoes import Preparacoes, PreparacaoId
from resource.cardapios import Cardapios, CardapioId
from resource.ingrediente_preparacao import IngredientesPreparacao, IngredientesPreparacaoId
from resource.cardapio_preparacao import CardapioPreparacoes, CardapioPreparacaoId
from resource.ficha_tecnica import FichaTecnicaOperacional, FichaTecnicaGerencial
from resource.unidade import Unidade, UnidadeId
from resource.medidaCaseira import MedidasCaseiras, MedidaCaseiraId
from resource.utensilios import Utensilios, UtensilioId

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:124356@localhost:5432/Pweb2"
from helpers.configCORS import cors
from resources.preparadores import Preparadores, PreparadorId
from resources.gestores import Gestores, GestorId
from resources.ingredientes import Ingredientes, IngredienteId
from resources.empresas import Empresas, EmpresaId
from resources.proprietarios import Proprietarios, ProprietarioId
from resources.preparacoes import Preparacoes, PreparacaoId
from resources.cardapios import Cardapios, CardapioId
from resources.preparacao_ingrediente import PreparacaoIngredientes, IngredientesPreparacaoId
from resources.cardapio_preparacao import CardapioPreapracoes, CardapioPreapracaoId
from resources.ficha_tecnica import FichaTecnicaOperacional, FichaTecnicaGerencial
from resources.unidade import Unidade, UnidadeId
from resources.medidaCaseira import MedidasCaseiras, MedidaCaseiraId
from resources.utensilios import Utensilios, UtensilioId
from resources.login import Login
from resources.logout import Logout
from resources.modo_preparo import ModosPreparo, ModosPreparoId

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:senhasecreta@localhost:5432/PreparoCerto"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
cors.init_app(app)
migrate.__init__(app, db)
api = Api(app)

api.add_resource(Gestores, '/gestor')
api.add_resource(GestorId, '/gestor/<int:id>')
api.add_resource(Preparadores, '/preparadores')
api.add_resource(PreparadorId, '/preparador/<int:id>')
api.add_resource(Ingredientes, '/ingredientes')
api.add_resource(IngredienteId, '/ingrediente/<int:id>')
api.add_resource(Empresas, '/empresas')
api.add_resource(EmpresaId, '/empresa/<int:id>')
api.add_resource(Proprietarios, '/proprietarios')
api.add_resource(ProprietarioId, '/proprietario/<int:id>')
api.add_resource(Preparacoes, '/preparacoes')
api.add_resource(PreparacaoId, '/preparacao/<int:id>')
api.add_resource(Cardapios, '/cardapios')
api.add_resource(CardapioId, '/cardapio/<int:id>')
api.add_resource(PreparacaoIngredientes, '/ingrediente_preparacao')
api.add_resource(IngredientesPreparacaoId, '/ingrediente_preparacao/<int:id>')
api.add_resource(CardapioPreparacoes, '/cardapio_preparacao')
api.add_resource(CardapioPreparacaoId, '/cardapio_preparacao/<int:id>')
api.add_resource(FichaTecnicaOperacional, '/fichatecnicaoperacional/<int:id>')
api.add_resource(FichaTecnicaGerencial, '/fichatecnicagerencial/<int:id>')
api.add_resource(Unidade, '/unidade')
api.add_resource(UnidadeId, '/unidade/<int:id>')
api.add_resource(MedidasCaseiras, '/medidas')
api.add_resource(MedidaCaseiraId, '/medidas/<int:id>')
api.add_resource(Utensilios, '/utensilios')
api.add_resource(UtensilioId, '/utensilio/<int:id>')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(ModosPreparo, '/modospreparo')
api.add_resource(ModosPreparoId, '/modospreparo/<int:id>')


if __name__ == '__main__':
    app.run(debug=True)
