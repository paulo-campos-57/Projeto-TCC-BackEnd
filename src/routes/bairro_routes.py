from flask import Blueprint, jsonify, request

from services.bairro_service import BairroService

bairro_bp = Blueprint('bairro_bp', __name__)


# Rota para encontrar bairro por ID
@bairro_bp.route('/<int:id_bairro>', methods=['GET'])
def get_bairro(id_bairro):
    bairro_obj = BairroService.gerar_configuracao_bairro(id_bairro)

    if bairro_obj.nome == 'Bairro Desconhecido':
        return jsonify({'error': 'Bairro não encontrado'}), 404

    return jsonify(bairro_obj.to_dict()), 200


# Rota para iniciar sessão (antes do jogo)
@bairro_bp.route('/iniciar_sessao', methods=['POST'])
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


# Rota para inicar jogo
@bairro_bp.route('/iniciar_jogo', methods=['POST'])
def iniciar_jogo():
    data = request.get_json()
    bairro_id = data.get('bairroId')
    tempo = data.get('tempoDeJogo')

    if not bairro_id or not tempo:
        return jsonify({'error': 'Dados incompletos para iniciar o jogo'}), 400

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
                    'inicio_timestamp': '2026-03-19T18:00:00',
                },
            }
        ),
        200,
    )


# Rota para listar todos os bairros
@bairro_bp.route('/lista', methods=['GET'])
def listar_bairros():
    bairros = BairroService.listar_todos()
    return jsonify([b.to_dict() for b in bairros]), 200
