from flask import Flask
from flask_restful import Api, Resource
from helpers.database import db, migrate
from resource.users import Users

app = Flask(__name__)

db.init_app(app)
migrate.__init__(app, db)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:senhasecreta@localhost:5432/Pweb2"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


api.add_resource(Users, '/')

if __name__ == '__main__':
  app.run(debug=True)