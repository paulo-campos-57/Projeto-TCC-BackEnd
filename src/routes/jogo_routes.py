from controllers.jogo_controller import JogoController
from flask import Blueprint

jogo_bp = Blueprint('jogo_bp', __name__)


@jogo_bp.route('/sessao', methods=['POST'])
def criar_sessao():
    """
    Cria uma nova sessão de jogo.
    Recebe as configurações iniciais (bairro e tempo). Se o token de autenticação
    for enviado no cabeçalho, a sessão será associada ao usuário para salvar o
    histórico no final.
    ---
    tags:
      - Jogo (Sessão)
    parameters:
      - name: Authorization
        in: header
        type: string
        required: false
        description: "Token JWT opcional. Formato: Bearer <token>"
      - in: body
        name: body
        required: true
        description: Dados iniciais para criar a sessão.
        schema:
          type: object
          required:
            - id_bairro
            - tempo_de_jogo
          properties:
            id_bairro:
              type: integer
              example: 1
            tempo_de_jogo:
              type: string
              example: "15 minutos"
    responses:
      201:
        description: >
          Sessão criada com sucesso. Retorna o ID, o estado
          e o catálogo do dia.
      400:
        description: Faltam parâmetros no corpo da requisição.
    """
    return JogoController.criar()


@jogo_bp.route('/sessao/<sessao_id>', methods=['GET'])
def estado_sessao(sessao_id):
    """
    Obtém o estado atual da sessão.
    Retorna um 'snapshot' público com todas as informações atuais do jogo
    daquela sessão específica.
    ---
    tags:
      - Jogo (Sessão)
    parameters:
      - name: sessao_id
        in: path
        type: string
        required: true
        description: ID da sessão de jogo em andamento.
    responses:
      200:
        description: Estado da sessão retornado com sucesso.
      404:
        description: Sessão não encontrada.
    """
    return JogoController.estado(sessao_id)


@jogo_bp.route('/sessao/<sessao_id>/comprar', methods=['POST'])
def comprar_ingrediente(sessao_id):
    """
    Compra um ingrediente no jogo.
    Debita o valor do saldo da sessão e adiciona o ingrediente ao estoque.
    ---
    tags:
      - Jogo (Ações)
    parameters:
      - name: sessao_id
        in: path
        type: string
        required: true
        description: ID da sessão de jogo.
      - in: body
        name: body
        required: true
        description: Nome do ingrediente a ser comprado.
        schema:
          type: object
          required:
            - nome
          properties:
            nome:
              type: string
              example: "Queijo Coalho"
    responses:
      200:
        description: Compra realizada com sucesso.
      400:
        description: Nome do ingrediente ausente.
      422:
        description: "Erro na regra de negócio (ex: saldo insuficiente)."
    """
    return JogoController.comprar(sessao_id)


@jogo_bp.route('/sessao/<sessao_id>/devolver', methods=['POST'])
def devolver_ingrediente(sessao_id):
    """
    Devolve um ingrediente ao catálogo.
    Remove o ingrediente do estoque e devolve o valor ao saldo da sessão.
    ---
    tags:
      - Jogo (Ações)
    parameters:
      - name: sessao_id
        in: path
        type: string
        required: true
        description: ID da sessão de jogo.
      - in: body
        name: body
        required: true
        description: Nome do ingrediente a ser devolvido.
        schema:
          type: object
          required:
            - nome
          properties:
            nome:
              type: string
              example: "Queijo Coalho"
    responses:
      200:
        description: Devolução realizada com sucesso.
      400:
        description: Nome do ingrediente ausente.
      422:
        description: "Erro na regra de negócio (ex: ingrediente não está no estoque)."
    """
    return JogoController.devolver(sessao_id)


@jogo_bp.route('/sessao/<sessao_id>/receita', methods=['PUT'])
def atualizar_receita(sessao_id):
    """
    Atualiza a proporção da receita da tapioca.
    Define as porções dos ingredientes que serão usados na montagem.
    ---
    tags:
      - Jogo (Ações)
    parameters:
      - name: sessao_id
        in: path
        type: string
        required: true
        description: ID da sessão de jogo.
      - in: body
        name: body
        required: true
        description: Objeto mapeando o nome do ingrediente para a quantidade de porções.
        schema:
          type: object
          required:
            - receita
          properties:
            receita:
              type: object
              example: {"Queijo Coalho": 2, "Coco Ralado": 1}
    responses:
      200:
        description: Receita atualizada com sucesso.
      400:
        description: Formato inválido da receita.
      422:
        description: Erro na regra de negócio.
    """
    return JogoController.receita(sessao_id)


@jogo_bp.route('/sessao/<sessao_id>/preco', methods=['PUT'])
def definir_preco(sessao_id):
    """
    Define o preço de venda da tapioca.
    ---
    tags:
      - Jogo (Ações)
    parameters:
      - name: sessao_id
        in: path
        type: string
        required: true
        description: ID da sessão de jogo.
      - in: body
        name: body
        required: true
        description: Novo preço de venda.
        schema:
          type: object
          required:
            - preco_tapioca
          properties:
            preco_tapioca:
              type: number
              format: float
              example: 10.50
    responses:
      200:
        description: Preço definido com sucesso.
      400:
        description: Preço não fornecido na requisição.
      422:
        description: Erro de validação.
    """
    return JogoController.preco(sessao_id)


@jogo_bp.route('/sessao/<sessao_id>/processar-dia', methods=['POST'])
def processar_dia_jogo(sessao_id):
    """
    Processa as vendas e eventos do dia.
    Calcula os ganhos, gastos, satisfação e possíveis eventos
    baseados no bairro e clima.
    ---
    tags:
      - Jogo (Progresso)
    parameters:
      - name: sessao_id
        in: path
        type: string
        required: true
        description: ID da sessão de jogo.
    responses:
      200:
        description: Dia processado com sucesso. Retorna os resultados do dia.
      409:
        description: Sessão de jogo já foi finalizada.
      422:
        description: "Erro na execução (ex: receita não configurada)."
    """
    return JogoController.processar_dia(sessao_id)


@jogo_bp.route('/sessao/<sessao_id>/avancar-dia', methods=['POST'])
def avancar_dia_jogo(sessao_id):
    """
    Avança o jogo para o dia seguinte.
    Atualiza o calendário do jogo e gera um novo catálogo de ingredientes.
    ---
    tags:
      - Jogo (Progresso)
    parameters:
      - name: sessao_id
        in: path
        type: string
        required: true
        description: ID da sessão de jogo.
    responses:
      200:
        description: Retorna o novo estado da sessão e o novo catálogo de compras.
    """
    return JogoController.avancar_dia(sessao_id)


@jogo_bp.route('/sessao/<sessao_id>', methods=['DELETE'])
def encerrar_sessao(sessao_id):
    """
    Encerra a sessão e salva o resultado final.
    Se o jogador iniciou a sessão autenticado, os resultados da partida
    são salvos no banco de dados. A sessão atual é descartada da memória.
    ---
    tags:
      - Jogo (Sessão)
    parameters:
      - name: sessao_id
        in: path
        type: string
        required: true
        description: ID da sessão a ser encerrada.
    responses:
      200:
        description: >
          Sessão encerrada. Retorna mensagem e os dados salvos
          do resultado (se aplicável).
    """
    return JogoController.encerrar(sessao_id)


@jogo_bp.route('/historico', methods=['GET'])
def buscar_historico():
    """
    Retorna o histórico de partidas do usuário.
    Busca no banco de dados todos os resultados salvos das partidas jogadas
    pelo usuário autenticado.
    ---
    tags:
      - Histórico
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: "Token JWT. Formato: Bearer <token>"
    responses:
      200:
        description: Uma lista com os resultados do histórico de partidas.
        schema:
          type: array
          items:
            type: object
      401:
        description: Token ausente, inválido ou expirado.
    """
    return JogoController.historico()
