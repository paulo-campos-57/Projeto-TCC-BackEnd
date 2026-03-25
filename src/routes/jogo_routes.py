from flask import Blueprint, jsonify, request

from models.ingrediente import Ingrediente
from models.sessao_jogo import criar_sessao, obter_sessao, remover_sessao
from services.jogo_service import JogoService

jogo_bp = Blueprint('jogo_bp', __name__)


# Rota para criar uma nova sessão de jogo
@jogo_bp.route('/sessao', methods=['POST'])
def criar():
    data = request.get_json()
    if not data:
        return jsonify({'erro': 'Corpo ausente.'}), 400

    id_bairro = data.get('id_bairro')
    tempo_de_jogo = data.get('tempo_de_jogo')

    if id_bairro is None or not tempo_de_jogo:
        return (
            jsonify(
                {'erro': "'id_bairro' e 'tempo_de_jogo' sao obrigatorios."}
            ),
            400,
        )

    sessao = criar_sessao(int(id_bairro), str(tempo_de_jogo))
    return (
        jsonify(
            {
                'sessao_id': sessao.sessao_id,
                'sessao': sessao.snapshot_publico(),
                'catalogo': Ingrediente.catalogo_para_cliente(),
            }
        ),
        201,
    )


# Rota para obter o estado atual da sessão
@jogo_bp.route('/sessao/<sessao_id>', methods=['GET'])
def estado(sessao_id: str):
    sessao = obter_sessao(sessao_id)
    if not sessao:
        return jsonify({'erro': 'Sessao nao encontrada.'}), 404
    return jsonify(sessao.snapshot_publico()), 200


# Rota para comprar um ingrediente
@jogo_bp.route('/sessao/<sessao_id>/comprar', methods=['POST'])
def comprar(sessao_id: str):
    sessao = obter_sessao(sessao_id)
    if not sessao:
        return jsonify({'erro': 'Sessao nao encontrada.'}), 404

    data = request.get_json()
    nome = (data or {}).get('nome')
    if not nome:
        return jsonify({'erro': "'nome' do ingrediente obrigatorio."}), 400

    resultado = sessao.comprar_ingrediente(nome)
    if not resultado['ok']:
        return jsonify(resultado), 422
    return jsonify(resultado), 200


# Rota para devolver um ingrediente
@jogo_bp.route('/sessao/<sessao_id>/devolver', methods=['POST'])
def devolver(sessao_id: str):
    sessao = obter_sessao(sessao_id)
    if not sessao:
        return jsonify({'erro': 'Sessao nao encontrada.'}), 404

    data = request.get_json()
    nome = (data or {}).get('nome')
    if not nome:
        return jsonify({'erro': "'nome' do ingrediente obrigatorio."}), 400

    resultado = sessao.devolver_ingrediente(nome)
    if not resultado['ok']:
        return jsonify(resultado), 422
    return jsonify(resultado), 200


# Rota para atualizar uma receita
@jogo_bp.route('/sessao/<sessao_id>/receita', methods=['PUT'])
def receita(sessao_id: str):
    sessao = obter_sessao(sessao_id)
    if not sessao:
        return jsonify({'erro': 'Sessao nao encontrada.'}), 404

    data = (request.get_json() or {}).get('receita')
    if not isinstance(data, dict):
        return (
            jsonify({'erro': "'receita' deve ser um objeto nome->porcao."}),
            400,
        )

    resultado = sessao.atualizar_receita({k: int(v) for k, v in data.items()})
    if not resultado['ok']:
        return jsonify(resultado), 422
    return jsonify(resultado), 200


# Rota para definir o preco da tapioca
@jogo_bp.route('/sessao/<sessao_id>/preco', methods=['PUT'])
def preco(sessao_id: str):
    sessao = obter_sessao(sessao_id)
    if not sessao:
        return jsonify({'erro': 'Sessao nao encontrada.'}), 404

    data = request.get_json()
    valor = (data or {}).get('preco_tapioca')
    if valor is None:
        return jsonify({'erro': "'preco_tapioca' obrigatorio."}), 400

    resultado = sessao.definir_preco(float(valor))
    if not resultado['ok']:
        return jsonify(resultado), 422
    return jsonify(resultado), 200


# Rota para processar o dia atual
@jogo_bp.route('/sessao/<sessao_id>/processar-dia', methods=['POST'])
def processar_dia(sessao_id: str):
    sessao = obter_sessao(sessao_id)
    if not sessao:
        return jsonify({'erro': 'Sessao nao encontrada.'}), 404

    if sessao.finalizado:
        return jsonify({'erro': 'Sessao ja finalizada.'}), 409

    resultado = JogoService.processar_dia(sessao)
    if 'erro' in resultado:
        return jsonify(resultado), 422

    return jsonify(resultado), 200


# Rota para avançar para o próximo dia
@jogo_bp.route('/sessao/<sessao_id>/avancar-dia', methods=['POST'])
def avancar_dia(sessao_id: str):
    sessao = obter_sessao(sessao_id)
    if not sessao:
        return jsonify({'erro': 'Sessao nao encontrada.'}), 404

    JogoService.avancar_dia(sessao)
    return (
        jsonify(
            {
                'sessao': sessao.snapshot_publico(),
                'catalogo': Ingrediente.catalogo_para_cliente(),
            }
        ),
        200,
    )


# Rota para encerrar a sessão
@jogo_bp.route('/sessao/<sessao_id>', methods=['DELETE'])
def encerrar(sessao_id: str):
    sessao = obter_sessao(sessao_id)
    if not sessao:
        return jsonify({'erro': 'Sessao nao encontrada.'}), 404
    remover_sessao(sessao_id)
    return jsonify({'mensagem': 'Sessao encerrada.'}), 200
