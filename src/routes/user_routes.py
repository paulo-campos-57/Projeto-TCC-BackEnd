from flask import Blueprint, jsonify, request

from services.user_service import UsuarioService

usuario_bp = Blueprint('usuario_bp', __name__)


# Rota de teste para verificar a conexão com o banco de dados
@usuario_bp.route('/')
def index():
    total = UsuarioService.contar_usuarios()
    return f'Conectado ao banco! Total de usuários: {total}'


# Rota para criação de novo usuário
@usuario_bp.route('/register', methods=['POST'])
def register():
    dados = request.json
    usuario = UsuarioService.criar_usuario(
        dados['nome'], dados['email'], dados['senha']
    )
    return jsonify({'message': 'Usuário criado!', 'id': usuario.id}), 201


# Rota para autenticação de usuário
@usuario_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('email') or not data.get('senha'):
        return jsonify({'error': 'Email e senha são obriatórios'}), 400

    usuario = UsuarioService.autenticar_usuario(data['email'], data['senha'])

    if usuario:
        return (
            jsonify(
                {
                    'Message': 'Login bem-sucedido',
                    'User': {
                        'id': str(usuario.id),
                        'nome': usuario.nome,
                        'email': usuario.email,
                    },
                }
            ),
            200,
        )

    return jsonify({'error': 'Credenciais inválidas'}), 401
