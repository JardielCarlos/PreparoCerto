from flask_restful import fields
from helpers.database import db
from werkzeug.security import generate_password_hash, check_password_hash

userFields = {'id': fields.Integer, 'nome': fields.String, 'email': fields.String, 'tipo':fields.String}

class Usuario(db.Model):
  __tablename__ = "tb_usuario"
  
  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String, nullable=False)
  email = db.Column(db.String, nullable=False, unique=True)
  senha = db.Column(db.String, nullable=False)
  tipo = db.Column(db.String, nullable=False)

  __mapper_args__ = {
    'polymorphic_identity': 'usuario',
    'polymorphic_on': tipo
  }
  
  def __init__(self, nome, email, senha):
    self.nome = nome
    self.email = email
    self.senha = generate_password_hash(senha)

  def verify_password(self, senha):
    return check_password_hash(self.senha, senha)

  def __repr__(self):
    return f"<User {self.nome}>"