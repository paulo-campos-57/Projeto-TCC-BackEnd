import os

from dotenv import load_dotenv
from flasgger import Swagger
from flask import Flask
from flask_cors import CORS
from routes.bairro_routes import bairro_bp
from routes.jogo_routes import jogo_bp
from routes.resultado_routes import resultado_bp
from routes.user_routes import usuario_bp

from database import db

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(
    app,
    resources={
        r'/*': {
            'origins': '*',
            'methods': ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
            'allow_headers': ['Content-Type', 'Authorization'],
        }
    },
)

db.init_app(app)

swagger_config = {
    'headers': [],
    'specs': [
        {
            'endpoint': 'apispec_1',
            'route': '/apispec_1.json',
            'rule_filter': lambda rule: True,
            'model_filter': lambda tag: True,
        }
    ],
    'static_url_path': '/flasgger_static',
    'swagger_ui': True,
    'specs_route': '/api-docs/',
}

swagger = Swagger(
    app,
    config=swagger_config,
    template={
        'info': {
            'title': 'API Tapiocaria Backend',
            'description': 'Documentação da API do backend do app Tapiocaria',
            'contact': {
                'name': 'Paulo Campos',
                'email': 'paulo.m.campos6601@gmail.com',
                'url': 'https://github.com/paulo-campos-57/Projeto-TCC-BackEnd/tree/main',
            },
            'version': '1.0.0',
        }
    },
)

app.register_blueprint(usuario_bp, url_prefix='/user')
app.register_blueprint(bairro_bp, url_prefix='/bairro')
app.register_blueprint(jogo_bp, url_prefix='/jogo')
app.register_blueprint(resultado_bp, url_prefix='/resultados')

with app.app_context():
    db.create_all()
    print('Banco de dados verificado/criado com sucesso!')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
