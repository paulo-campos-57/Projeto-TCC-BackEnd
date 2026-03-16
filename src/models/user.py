from database import db
import sqlalchemy as sa

class Usuario(db.Model):
    __tablename__ = 'user_table'
    __table_args__ = {'schema': 'tpdbc'}

    id = db.Column(sa.Text, primary_key=True)
    nome = db.Column(sa.String(100), nullable=False)
    email = db.Column(sa.String(255), unique=True, nullable=False)
    senha_hash = db.Column(sa.Text, nullable=False)