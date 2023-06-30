from helpers.database import db

class ImgPreparacao(db.Model):
  __tablename__ = "tb_imgpreparacao"

  id = db.Column(db.Integer, primary_key=True)
  fotoPerfil = db.Column(db.LargeBinary, nullable=True)

  preparacao = db.relationship("Preparacao")

  def __init__(self, fotoPerfil):
    self.fotoPerfil = fotoPerfil

  def __repr__(self):
    return f"<ImgPreparacao {self.fotoPerfil}"

