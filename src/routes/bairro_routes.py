from flask import Blueprint, jsonify, request

from services.bairro_service import BairroService

bairro_bp = Blueprint('bairro_bp', __name__)


@bairro_bp.route('/<int:id_bairro>', methods=['GET'])
def get_bairro(id_bairro):
    bairro_obj = BairroService.gerar_configuracao_bairro(id_bairro)

    if bairro_obj.nome == 'Bairro Desconhecido':
        return jsonify({'error': 'Bairro não encontrado'}), 404

    return jsonify(bairro_obj.to_dict()), 200


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


@bairro_bp.route('/lista', methods=['GET'])
def listar_bairros():
    bairros = BairroService.listar_todos()
    return jsonify([b.to_dict() for b in bairros]), 200
