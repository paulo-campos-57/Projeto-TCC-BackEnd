from controllers.jogo_controller import JogoController
from flask import Blueprint

jogo_bp = Blueprint('jogo_bp', __name__)


# iniciar sessão
@jogo_bp.route('/sessao', methods=['POST'])
def criar():
    return JogoController.criar()


# obter estado da sessão
@jogo_bp.route('/sessao/<sessao_id>', methods=['GET'])
def estado(sessao_id):
    return JogoController.estado(sessao_id)


# comprar ingrediente
@jogo_bp.route('/sessao/<sessao_id>/comprar', methods=['POST'])
def comprar(sessao_id):
    return JogoController.comprar(sessao_id)


# devolver ingrediente
@jogo_bp.route('/sessao/<sessao_id>/devolver', methods=['POST'])
def devolver(sessao_id):
    return JogoController.devolver(sessao_id)


# atualizar receita
@jogo_bp.route('/sessao/<sessao_id>/receita', methods=['PUT'])
def receita(sessao_id):
    return JogoController.receita(sessao_id)


# atualizar preço
@jogo_bp.route('/sessao/<sessao_id>/preco', methods=['PUT'])
def preco(sessao_id):
    return JogoController.preco(sessao_id)


# processar dia
@jogo_bp.route('/sessao/<sessao_id>/processar-dia', methods=['POST'])
def processar_dia(sessao_id):
    return JogoController.processar_dia(sessao_id)


# avançar dia
@jogo_bp.route('/sessao/<sessao_id>/avancar-dia', methods=['POST'])
def avancar_dia(sessao_id):
    return JogoController.avancar_dia(sessao_id)


# encerrar sessão
@jogo_bp.route('/sessao/<sessao_id>', methods=['DELETE'])
def encerrar(sessao_id):
    return JogoController.encerrar(sessao_id)
