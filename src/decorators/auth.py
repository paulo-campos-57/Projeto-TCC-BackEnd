import os
from functools import wraps

import jwt
from flask import jsonify, request


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        token = None

        if auth_header and ' ' in auth_header:
            token = auth_header.split(' ')[1].replace('"', '').strip()

        if not token:
            return jsonify({'error': 'Token de autenticação ausente'}), 401

        try:
            payload = jwt.decode(
                token, os.getenv('JWT_KEY'), algorithms=['HS256']
            )
            request.user_id = payload['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token inválido'}), 401
        except Exception as e:
            return (
                jsonify(
                    {'error': 'Erro ao processar token', 'details': str(e)}
                ),
                500,
            )

        return f(*args, **kwargs)

    return decorated
