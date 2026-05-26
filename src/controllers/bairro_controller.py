from datetime import datetime

from decorators.error_handler import handle_errors
from flask import jsonify, request

from services.bairro_service import BairroService


class BairroController:
    @staticmethod
    @handle_errors
    def get_bairro(id_bairro):
        bairro_obj = BairroService.buscar_por_id(id_bairro)

        if not bairro_obj or bairro_obj.nome == 'Bairro Desconhecido':
            return jsonify({'error': 'Bairro não encontrado'}), 404

        return jsonify(bairro_obj.to_dict()), 200

    @staticmethod
    @handle_errors
    def iniciar_sessao():
        data = request.get_json()
        tempo = data.get('tempo')

        if not tempo:
            return jsonify({'error': 'Tempo de jogo não selecionado'}), 400

        return (
            jsonify(
                {
                    'status': 'success',
                    'message': f'Jogo de {tempo} iniciado!',
                    'redirect_to': '/PaginaJogoCadastro',
                    'tempoDeJogo': tempo,
                }
            ),
            200,
        )

    @staticmethod
    @handle_errors
    def iniciar_jogo():
        data = request.get_json()
        bairro_id = data.get('bairroId')
        tempo = data.get('tempoDeJogo')

        if not bairro_id or not tempo:
            return (
                jsonify({'error': 'Dados incompletos para iniciar o jogo'}),
                400,
            )

        bairro = BairroService.buscar_por_id(bairro_id)
        if not bairro:
            return jsonify({'error': 'Bairro inválido'}), 404

        return (
            jsonify(
                {
                    'redirect_url': '/TelaDeJogoCadastro',
                    'game_config': {
                        'bairro': bairro.to_dict(),
                        'tempoDeJogo': tempo,
                        'inicio_timestamp': datetime.now().isoformat(),
                    },
                }
            ),
            200,
        )

    @staticmethod
    @handle_errors
    def listar_bairros():
        bairros = BairroService.listar_todos()
        return jsonify([b.to_dict() for b in bairros]), 200
