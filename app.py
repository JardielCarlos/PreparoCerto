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
from resource.cardapio_preparacao import CardapioPreapracoes, CardapioPreapracaoId
from resource.ficha_tecnica import FichaTecnicaOperacional, FichaTecnicaGerencial
from resource.unidade import Unidade, UnidadeId
from resource.medidaCaseira import MedidasCaseiras, MedidaCaseiraId
from resource.utensilios import Utensilios, UtensilioId

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:senhasecreta@localhost:5432/Pweb2"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate.__init__(app, db)
api = Api(app)

api.add_resource(Gestores, '/gestores')
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
api.add_resource(IngredientesPreparacao, '/ingrediente_preparacao')
api.add_resource(IngredientesPreparacaoId, '/ingrediente_preparacao/<int:id>')
api.add_resource(CardapioPreapracoes, '/cardapio_preparacao')
api.add_resource(CardapioPreapracaoId, '/cardapio_preparacao/<int:id>')
api.add_resource(FichaTecnicaOperacional, '/fichatecnicaoperacional/<int:id>')
api.add_resource(FichaTecnicaGerencial, '/fichatecnicagerencial/<int:id>')

api.add_resource(Unidade, '/unidade')
api.add_resource(UnidadeId, '/unidade/<int:id>')
api.add_resource(MedidasCaseiras, '/medidas')
api.add_resource(MedidaCaseiraId, '/medidas/<int:id>')

api.add_resource(Utensilios, '/utensilios')
api.add_resource(UtensilioId, '/utensilio/<int:id>')

if __name__ == '__main__':
  app.run(debug=True)