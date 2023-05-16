from flask import Flask
from flask_restful import Api, Resource
from helpers.database import db, migrate
from resource.usuarios import Usuarios

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:senhasecreta@localhost:5432/Pweb2"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate.__init__(app, db)
api = Api(app)


api.add_resource(Usuarios, '/')

if __name__ == '__main__':
  app.run(debug=True)