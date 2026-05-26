from controllers.bairro_controller import BairroController
from flask import Blueprint

bairro_bp = Blueprint('bairro_bp', __name__)


# listar todos os bairros
@bairro_bp.route('/lista', methods=['GET'])
def listar_bairros():
    """
    Lista todos os bairros cadastrados.
    Chama o BairroService para buscar e retornar uma lista completa de todos os
    bairros salvos no banco de dados.
    ---
    tags:
      - Bairros
    responses:
      200:
        description: Uma lista de objetos de bairros.
        schema:
          type: array
          items:
            type: object
    """
    return BairroController.listar_bairros()


# encontrar bairro por ID
@bairro_bp.route('/<int:id_bairro>', methods=['GET'])
def get_bairro(id_bairro):
    """
    Busca as informações de um bairro específico.
    O Controller recebe o ID pela URL e aciona o Service para verificar se o bairro
    existe no banco de dados.
    ---
    tags:
      - Bairros
    parameters:
      - in: path
        name: id_bairro
        type: integer
        required: true
        description: ID do bairro a ser buscado.
    responses:
      200:
        description: Dados do bairro retornados com sucesso.
      404:
        description: Bairro não encontrado ou desconhecido.
    """
    return BairroController.get_bairro(id_bairro)


# iniciar sessão
@bairro_bp.route('/iniciar_sessao', methods=['POST'])
def iniciar_sessao():
    """
    Inicia a sessão com o tempo de jogo.
    Recebe do frontend o tempo de jogo selecionado e retorna as informações de
    status e a URL para qual o usuário deve ser redirecionado.
    ---
    tags:
      - Sessão / Jogo
    parameters:
      - in: body
        name: body
        required: true
        description: Informações da sessão a ser iniciada.
        schema:
          type: object
          required:
            - tempo
          properties:
            tempo:
              type: string
              example: "1 semana"
    responses:
      200:
        description: Sessão iniciada com sucesso com dados para redirecionamento.
      400:
        description: Tempo de jogo não foi selecionado na requisição.
    """
    return BairroController.iniciar_sessao()


# iniciar jogo
@bairro_bp.route('/iniciar_jogo', methods=['POST'])
def iniciar_jogo():
    """
    Configura e inicia a partida do jogo.
    O Controller recebe o ID do bairro e o tempo de jogo selecionados. Ele valida
    o bairro no banco de dados e monta o objeto `game_config` com o timestamp atual
    para marcar o início exato da partida.
    ---
    tags:
      - Sessão / Jogo
    parameters:
      - in: body
        name: body
        required: true
        description: Dados do bairro e tempo escolhidos pelo jogador.
        schema:
          type: object
          required:
            - bairroId
            - tempoDeJogo
          properties:
            bairroId:
              type: integer
              example: 1
            tempoDeJogo:
              type: string
              example: "15 minutos"
    responses:
      200:
        description: Configurações do jogo geradas com sucesso.
      400:
        description: Faltam dados na requisição (bairroId ou tempoDeJogo).
      404:
        description: O ID do bairro fornecido é inválido.
    """
    return BairroController.iniciar_jogo()
