from controllers.resultado_controller import ResultadoController
from flask import Blueprint

resultado_bp = Blueprint('resultados', __name__)


@resultado_bp.route('/<user_id>/estatisticas', methods=['GET'])
def get_stats(user_id):
    """
    Obtém as estatísticas detalhadas de um usuário.
    Retorna dados agregados (lucro acumulado, melhor lucro, média de satisfação)
    e dados formatados para construção de gráficos de evolução financeira.
    ---
    tags:
      - Resultados e Estatísticas
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: "Token JWT obrigatório. Formato: Bearer <token>"
      - name: user_id
        in: path
        type: string
        required: true
        description: ID único do usuário (UUID).
    responses:
      200:
        description: Estatísticas retornadas com sucesso.
        schema:
          type: object
          properties:
            geral:
              type: object
              properties:
                total_partidas:
                  type: integer
                  example: 10
                lucro_acumulado:
                  type: number
                  example: 500.50
                media_satisfacao:
                  type: number
                  example: 4.5
                melhor_lucro:
                  type: number
                  example: 120.00
            graficos:
              type: object
              properties:
                labels:
                  type: array
                  items:
                    type: string
                  example: ["20/04", "21/04", "22/04"]
                lucro_por_partida:
                  type: array
                  items:
                    type: number
                  example: [45.0, 60.5, 30.0]
                satisfacao_por_partida:
                  type: array
                  items:
                    type: number
                  example: [4.0, 5.0, 4.5]
      401:
        description: Token ausente, inválido ou expirado.
      404:
        description: Nenhum resultado encontrado para este usuário.
    """
    return ResultadoController.get_user_stats(user_id)


@resultado_bp.route('/ranking', methods=['GET'])
def get_ranking():
    """
    Retorna o ranking global de jogadores.
    Permite filtrar os resultados por bairro e definir o critério de ordenação
    (lucro, satisfação ou faturamento). Retorna o top 10 resultados.
    ---
    tags:
      - Resultados e Estatísticas
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: "Token JWT obrigatório. Formato: Bearer <token>"
      - name: bairro
        in: query
        type: string
        required: false
        description: "Nome do bairro para filtrar (Ex: Casa Forte, Ibura, etc)."
      - name: ordenar
        in: query
        type: string
        required: false
        enum: [lucro, satisfacao, faturamento]
        default: lucro
        description: "Critério de ordenação do ranking."
    responses:
      200:
        description: Lista do ranking retornada com sucesso.
        schema:
          type: array
          items:
            type: object
            properties:
              posicao:
                type: integer
                example: 1
              nome:
                type: string
                example: "Jogador_01"
              bairro:
                type: string
                example: "Casa Forte"
              lucro:
                type: number
                example: 250.75
              satisfacao:
                type: number
                example: 4.8
              data:
                type: string
                example: "24/04/2026"
      401:
        description: Token ausente, inválido ou expirado.
    """
    return ResultadoController.get_ranking()
