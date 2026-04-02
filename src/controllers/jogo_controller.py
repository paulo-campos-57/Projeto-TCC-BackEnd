from decorators.error_handler import handle_errors
from flask import jsonify, request

from models.ingrediente import Ingrediente
from models.sessao_jogo import criar_sessao, obter_sessao, remover_sessao
from services.jogo_service import JogoService


class JogoController:
    @staticmethod
    @handle_errors
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

    @staticmethod
    @handle_errors
    def estado(sessao_id):
        sessao = obter_sessao(sessao_id)
        if not sessao:
            return jsonify({'erro': 'Sessao nao encontrada.'}), 404
        return jsonify(sessao.snapshot_publico()), 200

    @staticmethod
    @handle_errors
    def comprar(sessao_id):
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

    @staticmethod
    @handle_errors
    def devolver(sessao_id):
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

    @staticmethod
    @handle_errors
    def receita(sessao_id):
        sessao = obter_sessao(sessao_id)
        if not sessao:
            return jsonify({'erro': 'Sessao nao encontrada.'}), 404

        data = (request.get_json() or {}).get('receita')
        if not isinstance(data, dict):
            return (
                jsonify(
                    {'erro': "'receita' deve ser um objeto nome->porcao."}
                ),
                400,
            )

        resultado = sessao.atualizar_receita(
            {k: int(v) for k, v in data.items()}
        )
        if not resultado['ok']:
            return jsonify(resultado), 422
        return jsonify(resultado), 200

    @staticmethod
    @handle_errors
    def preco(sessao_id):
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

    @staticmethod
    @handle_errors
    def processar_dia(sessao_id):
        sessao = obter_sessao(sessao_id)
        if not sessao:
            return jsonify({'erro': 'Sessao nao encontrada.'}), 404

        if sessao.finalizado:
            return jsonify({'erro': 'Sessao ja finalizada.'}), 409

        resultado = JogoService.processar_dia(sessao)
        if 'erro' in resultado:
            return jsonify(resultado), 422

        return jsonify(resultado), 200

    @staticmethod
    @handle_errors
    def avancar_dia(sessao_id):
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

    @staticmethod
    @handle_errors
    def encerrar(sessao_id):
        sessao = obter_sessao(sessao_id)
        if not sessao:
            return jsonify({'erro': 'Sessao nao encontrada.'}), 404
        remover_sessao(sessao_id)
        return jsonify({'mensagem': 'Sessao encerrada.'}), 200
