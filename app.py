from flask import Flask
from flask_restful import Api
from helpers.database import db, migrate
from resource.usuarios import Usuarios
from resource.Gestores import Gestores
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:senhasecreta@localhost:5432/Pweb2"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)
db.init_app(app)
migrate.__init__(app, db)
api = Api(app)



api.add_resource(Usuarios, '/')
api.add_resource(Gestores, '/gestor')

if __name__ == '__main__':
  app.run(debug=True)