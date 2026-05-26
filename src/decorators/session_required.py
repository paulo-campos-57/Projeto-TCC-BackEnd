from functools import wraps

from flask import jsonify

from models.sessao_jogo import obter_sessao


def session_required(f):
    @wraps(f)
    def decorated_function(sessao_id, *args, **kwargs):
        sessao = obter_sessao(sessao_id)
        if not sessao:
            return jsonify({'erro': 'Sessao nao encontrada.'}), 404
        return f(sessao, *args, **kwargs)

    return decorated_function
