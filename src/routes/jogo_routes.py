from flask import Blueprint, jsonify, request

from services.jogo_service import JogoService

jogo_bp = Blueprint("jogo_bp", __name__)


# Rota para processar o dia de vendas
@jogo_bp.route("/processar-dia", methods=["POST"])
def processar_dia():
    data = request.get_json()

    if not data:
        return jsonify({"erro": "Corpo da requisição ausente."}), 400

    id_bairro = data.get("id_bairro")
    preco_tapioca = data.get("preco_tapioca")
    estoque_disponivel = data.get("estoque_disponivel")

    if any(v is None for v in [id_bairro, preco_tapioca, estoque_disponivel]):
        return (
            jsonify(
                {
                    "erro": (
                        "Campos 'id_bairro', 'preco_tapioca' e "
                        "'estoque_disponivel' são obrigatórios."
                    )
                }
            ),
            400,
        )

    if not isinstance(preco_tapioca, (int, float)) or preco_tapioca <= 0:
        return jsonify({"erro": "Preço deve ser um número positivo."}), 422

    if not isinstance(estoque_disponivel, int) or estoque_disponivel < 0:
        return (
            jsonify({"erro": "Estoque deve ser um inteiro não-negativo."}),
            422,
        )

    resultado = JogoService.processar_dia(
        id_bairro=int(id_bairro),
        preco_tapioca=float(preco_tapioca),
        estoque_disponivel=int(estoque_disponivel),
    )

    if "erro" in resultado:
        return jsonify(resultado), 404

    return jsonify(resultado), 200
