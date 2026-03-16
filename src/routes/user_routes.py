from flask import Blueprint, jsonify, request
from services.user_service import UsuarioService

usuario_bp = Blueprint("usuario_bp", __name__)


@usuario_bp.route("/")
def index():
    total = UsuarioService.contar_usuarios()
    return f"Conectado ao banco! Total de usuários: {total}"


@usuario_bp.route("/register", methods=["POST"])
def register():
    dados = request.json
    usuario = UsuarioService.criar_usuario(
        dados["nome"], dados["email"], dados["senha"]
    )
    return jsonify({"message": "Usuário criado!", "id": usuario.id}), 201
