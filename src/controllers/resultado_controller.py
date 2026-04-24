from decorators.error_handler import handle_errors
from flask import jsonify

from services.resultado_service import ResultadoService


class ResultadoController:
    @staticmethod
    @handle_errors
    def get_user_stats(user_id):
        stats = ResultadoService.obter_estatisticas(user_id)

        if not stats:
            raise ValueError('Nenhum resultado encontrado para este usuário.')

        return jsonify(stats), 200
