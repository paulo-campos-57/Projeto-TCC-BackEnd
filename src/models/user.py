from database import db
import sqlalchemy as sa

from sqlalchemy.dialects.postgresql import UUID


class Usuario(db.Model):
    __tablename__ = "user_table"
    __table_args__ = {"schema": "public"}

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=sa.text("gen_random_uuid()"),
    )
    nome = db.Column("user_name", db.String(100), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    senha_hash = db.Column("hash_pass", db.Text, nullable=False)
