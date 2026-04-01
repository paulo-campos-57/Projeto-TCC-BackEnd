from controllers.user_controller import UserController
from flask import Blueprint, jsonify

from services.user_service import UserService

usuario_bp = Blueprint('usuario_bp', __name__)


# rota de teste
@usuario_bp.route('/')
def index():
    total = UserService.contar_usuarios()
    return f'Conectado ao banco! Total de usuários: {total}'


# cadastro
@usuario_bp.route('/register', methods=['POST'])
def register():
    return UserController.register()


# login
@usuario_bp.route('/login', methods=['POST'])
def login():
    return UserController.login()


# logout
@usuario_bp.route('/logout', methods=['POST'])
def logout():
    return jsonify({'message': 'Logout bem-sucedido!'}), 200


# perfil de usuário
@usuario_bp.route('/me', methods=['GET'])
def get_user_logged():
    return UserController.get_me()


# atualização de usuário
@usuario_bp.route('/update/<string:usuario_id>', methods=['PUT'])
def update_usuario(usuario_id):
    return UserController.update(usuario_id)


# exclusão de usuário
@usuario_bp.route('/delete/<string:usuario_id>', methods=['DELETE'])
def delete_usuario(usuario_id):
    return UserController.delete(usuario_id)
