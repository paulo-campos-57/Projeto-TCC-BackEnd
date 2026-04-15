from controllers.user_controller import UserController
from flask import Blueprint, jsonify

from services.user_service import UserService

usuario_bp = Blueprint('usuario_bp', __name__)


# rota de teste
@usuario_bp.route('/')
def index():
    """
    Verifica a conexão com o banco e o total de usuários.
    Esta rota chama o UserService para realizar um count() no banco de dados
    e verificar se a aplicação está conectada corretamente.
    ---
    tags:
      - Testes
    responses:
      200:
        description: Retorna uma string confirmando a conexão e o total.
    """
    total = UserService.contar_usuarios()
    return f'Conectado ao banco! Total de usuários: {total}'


# cadastro
@usuario_bp.route('/register', methods=['POST'])
def register():
    """
    Cadastra um novo usuário no sistema.
    Recebe os dados via JSON, repassa para o UserController validar os campos
    e depois para o UserService aplicar o hash na senha e salvar no banco de dados.
    ---
    tags:
      - Autenticação
    parameters:
      - in: body
        name: body
        required: true
        description: Dados necessários para criar a conta.
        schema:
          type: object
          required:
            - nome
            - email
            - senha
          properties:
            nome:
              type: string
              example: "Maria Souza"
            email:
              type: string
              example: "maria@email.com"
            senha:
              type: string
              example: "senha_segura_123"
    responses:
      201:
        description: Usuário criado com sucesso!
      400:
        description: Erro de validação ou dados incorretos.
    """
    return UserController.register()


# login
@usuario_bp.route('/login', methods=['POST'])
def login():
    """
    Autentica o usuário e gera o Token JWT.
    O Controller recebe as credenciais, o Service busca o usuário no banco
    e compara o hash da senha. Se tudo estiver correto, o Controller gera
    um Token JWT com validade de 24 horas.
    ---
    tags:
      - Autenticação
    parameters:
      - in: body
        name: body
        required: true
        description: Credenciais de acesso.
        schema:
          type: object
          required:
            - email
            - senha
          properties:
            email:
              type: string
              example: "maria@email.com"
            senha:
              type: string
              example: "senha_segura_123"
    responses:
      200:
        description: Login bem-sucedido. Retorna os dados do usuário e o Token JWT.
      400:
        description: Campos obrigatórios ausentes.
      401:
        description: E-mail ou senha incorretos.
    """
    return UserController.login()


# logout
@usuario_bp.route('/logout', methods=['POST'])
def logout():
    """
    Realiza o logout do usuário.
    Como estamos usando JWT (que é stateless), o logout real ocorre no frontend
    (apagando o token armazenado). Esta rota serve apenas como uma confirmação
    de ação para o cliente.
    ---
    tags:
      - Autenticação
    responses:
      200:
        description: Mensagem de confirmação de logout.
    """
    return jsonify({'message': 'Logout bem-sucedido!'}), 200


# perfil de usuário
@usuario_bp.route('/me', methods=['GET'])
def get_user_logged():
    """
    Busca os dados do perfil do usuário logado.
    A rota é protegida e extrai o ID do usuário diretamente do Token JWT recebido
    no header. O Service faz a busca por esse ID e retorna os dados seguros.
    ---
    tags:
      - Usuários (Área Protegida)
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: "Token JWT. Formato: Bearer <token>"
    responses:
      200:
        description: Dados do perfil retornados com sucesso.
      401:
        description: Token inválido ou ausente.
      404:
        description: Usuário não encontrado no banco.
    """
    return UserController.get_me()


# atualização de usuário
@usuario_bp.route('/update_me', methods=['PUT'])
def update_usuario():
    """
    Atualiza as informações do usuário logado.
    Utiliza o ID contido no Token JWT para garantir que o usuário só possa
    alterar os próprios dados. O Service aplica as modificações no banco.
    ---
    tags:
      - Usuários (Área Protegida)
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: "Token JWT. Formato: Bearer <token>"
      - in: body
        name: body
        required: true
        description: Dados que serão atualizados.
        schema:
          type: object
          properties:
            nome:
              type: string
              example: "Maria Souza Silva"
            email:
              type: string
              example: "maria.nova@email.com"
    responses:
      200:
        description: Perfil atualizado com sucesso.
      401:
        description: Token inválido ou ausente.
      404:
        description: Usuário não encontrado.
    """
    return UserController.update()


# exclusão de usuário
@usuario_bp.route('/delete', methods=['DELETE'])
def delete_usuario():
    """
    Exclui a conta do usuário logado.
    Identifica o usuário pelo Token JWT e aciona o Service para remover
    o registro correspondente do banco de dados permanentemente.
    ---
    tags:
      - Usuários (Área Protegida)
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: "Token JWT. Formato: Bearer <token>"
    responses:
      200:
        description: Conta excluída com sucesso.
      401:
        description: Token inválido ou ausente.
      404:
        description: Usuário não encontrado.
    """
    return UserController.delete()
