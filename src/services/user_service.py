import bcrypt
from database import db
from models.user import Usuario


class UsuarioService:
    @staticmethod
    def criar_usuario(nome, email, senha_plana):
        salt = bcrypt.gensalt()
        hash_senha = bcrypt.hashpw(senha_plana.encode("utf-8"), salt)

        novo_usuario = Usuario(
            nome=nome, email=email, senha_hash=hash_senha.decode("utf-8")
        )

        db.session.add(novo_usuario)
        db.session.commit()
        return novo_usuario

    @staticmethod
    def contar_usuarios():
        return Usuario.query.count()
