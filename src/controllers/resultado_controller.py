from decorators.error_handler import handle_errors
from flask import jsonify, request

from services.resultado_service import ResultadoService


class ResultadoController:
    @staticmethod
    @handle_errors
    def get_user_stats(user_id):
        stats = ResultadoService.obter_estatisticas(user_id)

        if not stats:
            raise ValueError('Nenhum resultado encontrado para este usuário.')

        return jsonify(stats), 200

    @staticmethod
    @handle_errors
    def get_ranking():
        bairro = request.args.get('bairro')
        ordenar = request.args.get('ordenar', 'lucro')

        ranking = ResultadoService.obter_ranking(bairro, ordenar)
        return jsonify(ranking), 200
