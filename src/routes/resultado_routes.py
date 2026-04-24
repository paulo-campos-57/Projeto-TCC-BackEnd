from controllers.resultado_controller import ResultadoController
from flask import Blueprint

resultado_bp = Blueprint('resultados', __name__)


@resultado_bp.route('/<user_id>/estatisticas', methods=['GET'])
def get_stats(user_id):
    return ResultadoController.get_user_stats(user_id)
