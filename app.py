from flask import Flask
from flask_restful import Api, Resource
from helpers.database import db, migrate
from resource.users import Users

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:senhasecreta@localhost:5432/Pweb2"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate.__init__(app, db)
api = Api(app)


class User(Resource):
  def get(self):
    return {'hello': 'Rhavy'}

api.add_resource(User, '/')

if __name__ == '__main__':
  app.run(debug=True)