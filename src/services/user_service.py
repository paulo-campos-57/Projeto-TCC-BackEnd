import bcrypt

from database import db
from models.user import Usuario


class UsuarioService:
    # Criação de usuário
    @staticmethod
    def criar_usuario(nome, email, senha_plana):
        salt = bcrypt.gensalt()
        hash_senha = bcrypt.hashpw(senha_plana.encode('utf-8'), salt)

        novo_usuario = Usuario(
            nome=nome, email=email, senha_hash=hash_senha.decode('utf-8')
        )

        db.session.add(novo_usuario)
        db.session.commit()
        return novo_usuario

    # Autenticação de usuário
    @staticmethod
    @staticmethod
    def autenticar_usuario(email, senha_plana):
        usuario = Usuario.query.filter_by(email=email).first()

        if not usuario:
            return None

        try:
            if bcrypt.checkpw(
                senha_plana.encode('utf-8'), usuario.senha_hash.encode('utf-8')
            ):
                return usuario
        except Exception as e:
            print(f'Erro técnico na verificação: {e}')
            return None

        return None

    # Contar o número total de usuários
    @staticmethod
    def contar_usuarios():
        return Usuario.query.count()

    # Excluir usuário por ID
    @staticmethod
    def excluir_usuario(usuario_id):
        usuario = Usuario.query.get(usuario_id)
        if usuario:
            db.session.delete(usuario)
            db.session.commit()
            return True
        return False

    # Atualizar usuário por ID
    @staticmethod
    def autalizar_usuario(usuario_id, dados):
        usuario = Usuario.query.get(usuario_id)

        if not usuario:
            return None

        if 'nome' in dados:
            usuario.nome = dados['nome']
        if 'email' in dados:
            usuario.email = dados['email']
        if 'senha' in dados and dados['senha']:
            salt = bcrypt.gensalt()
            hash_senha = bcrypt.hashpw(dados['senha'].encode('utf-8'), salt)
            usuario.senha_hash = hash_senha.decode('utf-8')

        db.session.commit()
        return usuario
