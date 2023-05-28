from flask import Flask
from flask_restful import Api
from helpers.database import db, migrate

from resource.preparadores import Preparadores, PreparadorId
from resource.gestores import Gestores, GestorId
from resource.ingrediente import Ingredientes, IngredienteId
from resource.empresa import Empresas, EmpresaId

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

if __name__ == '__main__':
  app.run(debug=True)