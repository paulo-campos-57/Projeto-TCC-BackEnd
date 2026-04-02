import os
from datetime import datetime, timedelta, timezone

import jwt
from decorators.auth import token_required
from decorators.error_handler import handle_errors
from flask import jsonify, request

from services.user_service import UserService


class UserController:
    @staticmethod
    @handle_errors
    def register():
        dados = request.json
        usuario = UserService.criar_usuario(
            dados['nome'], dados['email'], dados['senha']
        )
        return jsonify({'message': 'Usuário criado!', 'id': usuario.id}), 201

    @staticmethod
    @handle_errors
    def login():
        data = request.get_json()
        if not data or not data.get('email') or not data.get('senha'):
            return jsonify({'error': 'Email e senha são obrigatórios'}), 400

        user = UserService.autenticar_usuario(data['email'], data['senha'])
        if not user:
            return jsonify({'error': 'Credenciais inválidas'}), 401

        payload = {
            'user_id': str(user.id),
            'exp': datetime.now(timezone.utc) + timedelta(hours=24),
        }
        token = jwt.encode(payload, os.getenv('JWT_KEY'), algorithm='HS256')

        return (
            jsonify(
                {
                    'Message': 'Login bem-sucedido',
                    'token': token,
                    'User': {
                        'id': str(user.id),
                        'nome': user.nome,
                        'email': user.email,
                    },
                }
            ),
            200,
        )

    @staticmethod
    @token_required
    @handle_errors
    def get_me():
        user = UserService.get_user_by_id(request.user_id)
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404

        return (
            jsonify(
                {
                    'User': {
                        'id': str(user.id),
                        'nome': user.nome,
                        'email': user.email,
                    }
                }
            ),
            200,
        )

    @staticmethod
    @token_required
    @handle_errors
    def delete():
        usuario_id = request.user_id
        if UserService.excluir_usuario(usuario_id):
            return jsonify({'message': 'Usuário excluído com sucesso!'}), 200
        return jsonify({'error': 'Usuário não encontrado'}), 404

    @staticmethod
    @token_required
    @handle_errors
    def update():
        usuario_id = request.user_id
        dados = request.get_json()
        user = UserService.atualizar_usuario(usuario_id, dados)

        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404

        return (
            jsonify(
                {
                    'message': 'Usuário atualizado com sucesso!',
                    'User': {'nome': user.nome, 'email': user.email},
                }
            ),
            200,
        )
