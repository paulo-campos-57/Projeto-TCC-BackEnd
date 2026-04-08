import os

import jwt as _jwt
from decorators.error_handler import handle_errors
from decorators.session_required import session_required
from flask import jsonify, request

from models.ingrediente import Ingrediente
from models.sessao_jogo import criar_sessao, remover_sessao
from services.bairro_service import BairroService
from services.jogo_service import JogoService
from services.resultado_service import ResultadoService


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

        auth = request.headers.get('Authorization', '')
        if auth.startswith('Bearer '):
            try:
                token = auth.split(' ')[1].replace('"', '').strip()
                payload = _jwt.decode(
                    token, os.getenv('JWT_KEY'), algorithms=['HS256']
                )
                sessao.user_id = payload.get('user_id')
            except Exception:
                pass

        return (
            jsonify(
                {
                    'sessao_id': sessao.sessao_id,
                    'sessao': sessao.snapshot_publico(),
                    'catalogo': Ingrediente.catalogo_para_cliente(
                        sessao.dia_atual
                    ),
                }
            ),
            201,
        )

    @staticmethod
    @handle_errors
    @session_required
    def estado(sessao):
        return jsonify(sessao.snapshot_publico()), 200

    @staticmethod
    @handle_errors
    @session_required
    def comprar(sessao):
        nome = (request.get_json() or {}).get('nome')
        if not nome:
            return jsonify({'erro': "'nome' do ingrediente obrigatorio."}), 400

        resultado = sessao.comprar_ingrediente(nome)
        return jsonify(resultado), (200 if resultado['ok'] else 422)

    @staticmethod
    @handle_errors
    @session_required
    def devolver(sessao):
        nome = (request.get_json() or {}).get('nome')
        if not nome:
            return jsonify({'erro': "'nome' do ingrediente obrigatorio."}), 400

        resultado = sessao.devolver_ingrediente(nome)
        return jsonify(resultado), (200 if resultado['ok'] else 422)

    @staticmethod
    @handle_errors
    @session_required
    def receita(sessao):
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
        return jsonify(resultado), (200 if resultado['ok'] else 422)

    @staticmethod
    @handle_errors
    @session_required
    def preco(sessao):
        valor = (request.get_json() or {}).get('preco_tapioca')
        if valor is None:
            return jsonify({'erro': "'preco_tapioca' obrigatorio."}), 400

        resultado = sessao.definir_preco(float(valor))
        return jsonify(resultado), (200 if resultado['ok'] else 422)

    @staticmethod
    @handle_errors
    @session_required
    def processar_dia(sessao):
        if sessao.finalizado:
            return jsonify({'erro': 'Sessao ja finalizada.'}), 409

        resultado = JogoService.processar_dia(sessao)
        return jsonify(resultado), (200 if 'erro' not in resultado else 422)

    @staticmethod
    @handle_errors
    @session_required
    def avancar_dia(sessao):
        JogoService.avancar_dia(sessao)
        return (
            jsonify(
                {
                    'sessao': sessao.snapshot_publico(),
                    'catalogo': Ingrediente.catalogo_para_cliente(
                        sessao.dia_atual
                    ),
                }
            ),
            200,
        )

    @staticmethod
    @handle_errors
    @session_required
    def encerrar(sessao):
        resultado_salvo = None
        if sessao.user_id:
            bairro = BairroService.buscar_por_id(sessao.id_bairro)
            nome_bairro = bairro.nome if bairro else 'Desconhecido'
            hist = sessao.satisfacao_historico or []
            sat_media = (
                round(sum(hist) / len(hist), 2)
                if hist
                else float(sessao.satisfacao)
            )

            try:
                r = ResultadoService.salvar_resultado(
                    user_id=sessao.user_id,
                    bairro=nome_bairro,
                    tempo_de_jogo=sessao.tempo_de_jogo,
                    dias_jogados=sessao.dia_atual,
                    faturamento=sessao.faturamento_total,
                    lucro_liquido=round(
                        sessao.faturamento_total - sessao.gasto_total, 2
                    ),
                    satisfacao_media=sat_media,
                    satisfacao_final=sessao.satisfacao,
                )
                resultado_salvo = r.to_dict()
            except Exception as e:
                resultado_salvo = {'erro': str(e)}

        remover_sessao(sessao.sessao_id)
        return (
            jsonify(
                {'mensagem': 'Sessao encerrada.', 'resultado': resultado_salvo}
            ),
            200,
        )

    @staticmethod
    @handle_errors
    def historico():
        auth = request.headers.get('Authorization', '')
        if not auth.startswith('Bearer '):
            return jsonify({'erro': 'Token ausente.'}), 401
        try:
            token = auth.split(' ')[1].replace('"', '').strip()
            payload = _jwt.decode(
                token, os.getenv('JWT_KEY'), algorithms=['HS256']
            )
            resultados = ResultadoService.listar_por_usuario(
                payload['user_id']
            )
            return jsonify([r.to_dict() for r in resultados]), 200
        except Exception:
            return jsonify({'erro': 'Token invalido ou expirado.'}), 401
