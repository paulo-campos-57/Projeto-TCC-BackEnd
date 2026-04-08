from controllers.jogo_controller import JogoController
from flask import Blueprint

jogo_bp = Blueprint('jogo_bp', __name__)

jogo_bp.route('/sessao', methods=['POST'])(JogoController.criar)
jogo_bp.route('/sessao/<sessao_id>', methods=['GET'])(JogoController.estado)
jogo_bp.route('/sessao/<sessao_id>/comprar', methods=['POST'])(
    JogoController.comprar
)
jogo_bp.route('/sessao/<sessao_id>/devolver', methods=['POST'])(
    JogoController.devolver
)
jogo_bp.route('/sessao/<sessao_id>/receita', methods=['PUT'])(
    JogoController.receita
)
jogo_bp.route('/sessao/<sessao_id>/preco', methods=['PUT'])(
    JogoController.preco
)
jogo_bp.route('/sessao/<sessao_id>/processar-dia', methods=['POST'])(
    JogoController.processar_dia
)
jogo_bp.route('/sessao/<sessao_id>/avancar-dia', methods=['POST'])(
    JogoController.avancar_dia
)
jogo_bp.route('/sessao/<sessao_id>', methods=['DELETE'])(
    JogoController.encerrar
)
jogo_bp.route('/historico', methods=['GET'])(JogoController.historico)
