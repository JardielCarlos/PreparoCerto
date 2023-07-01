from helpers.database import db

class ImgPreparacao(db.Model):
  __tablename__ = "tb_imgpreparacao"

  id = db.Column(db.Integer, primary_key=True)
  fotoPerfil = db.Column(db.LargeBinary, nullable=True)
  preparacao_id = db.Column(db.Integer, db.ForeignKey("tb_preparacao.id"))

  preparacao = db.relationship("Preparacao",uselist=False, back_populates="imagens")

  def __init__(self, fotoPerfil, preparacao_id):
    self.fotoPerfil = fotoPerfil
    self.preparacao = preparacao_id

  def __repr__(self):
    return f"<ImgPreparacao {self.fotoPerfil}"

