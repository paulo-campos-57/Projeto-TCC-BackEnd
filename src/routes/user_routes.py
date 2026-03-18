import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from flask import Blueprint, jsonify, request

from models.user import Usuario
from services.user_service import UsuarioService

load_dotenv()


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

    if not usuario:
        return jsonify({'error': 'Credenciais inválidas'}), 401

    if usuario:
        payload = {
            'user_id': str(usuario.id),
            'exp': datetime.now(timezone.utc) + timedelta(hours=24),
        }

        token = jwt.encode(payload, os.getenv('JWT_KEY'), algorithm='HS256')

        return (
            jsonify(
                {
                    'Message': 'Login bem-sucedido',
                    'token': token,
                    'User': {
                        'nome': usuario.nome,
                        'email': usuario.email,
                    },
                }
            ),
            200,
        )

    return jsonify({'error': 'Credenciais inválidas'}), 401


# Rota de logout
@usuario_bp.route('/logout', methods=['POST'])
def logout():
    return jsonify({'message': 'Logout bem-sucedido!'}), 200


# Rota para excluir usuário por ID
@usuario_bp.route('/delete/<string:usuario_id>', methods=['DELETE'])
def delete_usuario(usuario_id):
    token_header = request.headers.get('Authorization')

    try:
        token = token_header.split(' ')[1].replace('"', '').strip()
        payload = jwt.decode(token, os.getenv('JWT_KEY'), algorithms=['HS256'])

        if payload['user_id'] != usuario_id:
            return jsonify({'error': 'Ação não autorizada!'}), 403
    except Exception as e:
        return jsonify({'error': 'Token inválido', 'details': str(e)}), 401

    if UsuarioService.excluir_usuario(usuario_id):
        return jsonify({'message': 'Usuário excluído com sucesso!'}), 200
    return jsonify({'error': 'Usuário não encontrado'}), 404


# Rota para obter dados do usuário logado
@usuario_bp.route('/me', methods=['GET'])
def get_user_logged():
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({'error': 'Token ausente'}), 401

    try:
        if 'Bearer ' in token:
            token = token.split(' ')[1]

        payload = jwt.decode(token, os.getenv('JWT_KEY'), algorithms=['HS256'])
        usuario_id = payload['user_id']

        usuario = Usuario.query.get(usuario_id)

        if not usuario:
            return jsonify({'error': 'Usuário não encontrado'}), 404

        return (
            jsonify(
                {
                    'User': {
                        'id': str(usuario.id),
                        'nome': usuario.nome,
                        'email': usuario.email,
                    }
                }
            ),
            200,
        )

    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expirado'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Token inválido'}), 401


# Rota para atualizar usuário
@usuario_bp.route('/update_me', methods=['PUT'])
def update_me():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'Token ausente'}), 401

    try:
        if 'Bearer ' in token:
            token = token.split(' ')[1]
        token = token.replace('"', '').strip()

        payload = jwt.decode(token, os.getenv('JWT_KEY'), algorithms=['HS256'])
        usuario_id = payload['user_id']

        dados = request.get_json()

        usuario_atualizado = UsuarioService.autalizar_usuario(
            usuario_id, dados
        )

        if not usuario_atualizado:
            return jsonify({'error': 'Usuário não encontrado'}), 404

        return (
            jsonify(
                {
                    'Message': 'Perfil atualizado com sucesso!',
                    'User': {
                        'nome': usuario_atualizado.nome,
                        'email': usuario_atualizado.email,
                    },
                }
            ),
            200,
        )

    except jwt.ExpiredSignatureError:
        return (
            jsonify({'error': 'Sessão expirada. Faça login novamente.'}),
            401,
        )
    except Exception as e:
        return jsonify({'error': f'Erro na autenticação: {str(e)}'}), 401
