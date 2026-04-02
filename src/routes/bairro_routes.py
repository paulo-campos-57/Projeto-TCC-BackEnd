from controllers.bairro_controller import BairroController
from flask import Blueprint

bairro_bp = Blueprint('bairro_bp', __name__)


# encontrar bairro por ID
@bairro_bp.route('/<int:id_bairro>', methods=['GET'])
def get_bairro(id_bairro):
    return BairroController.get_bairro(id_bairro)


# iniciar sessão
@bairro_bp.route('/iniciar_sessao', methods=['POST'])
def iniciar_sessao():
    return BairroController.iniciar_sessao()


# iniciar jogo
@bairro_bp.route('/iniciar_jogo', methods=['POST'])
def iniciar_jogo():
    return BairroController.iniciar_jogo()


# listar todos os bairros
@bairro_bp.route('/lista', methods=['GET'])
def listar_bairros():
    return BairroController.listar_bairros()
