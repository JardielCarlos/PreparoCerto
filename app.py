from flask import Flask
from flask_restful import Api, Resource
from helpers.database import db, migrate

app = Flask(__name__)

db.init_app(app)
migrate.__init__(app, db)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:senhasecreta@localhost:5432/Pweb2"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



class User(Resource):
  def get(self):
    return {'hell|o': 'world'}

api.add_resource(User, '/')

if __name__ == '__main__':
  app.run(debug=True)