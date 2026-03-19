from flask import Blueprint, jsonify

from services.bairro_service import BairroService

bairro_bp = Blueprint('bairro_bp', __name__)


@bairro_bp.route('/<int:id_bairro>', methods=['GET'])
def get_bairro(id_bairro):
    bairro_obj = BairroService.gerar_configuracao_bairro(id_bairro)

    if bairro_obj.nome == 'Bairro Desconhecido':
        return jsonify({'error': 'Bairro não encontrado'}), 404

    return jsonify(bairro_obj.to_dict()), 200


@bairro_bp.route('/lista', methods=['GET'])
def listar_bairros():
    lista = [
        {'id': k, 'nome': v['nome']}
        for k, v in BairroService.CONFIGURACOES_BAIRROS.items()
    ]
    return jsonify(lista), 200
