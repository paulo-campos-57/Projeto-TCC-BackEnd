import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from routes.bairro_routes import bairro_bp
from routes.jogo_routes import jogo_bp
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

app.register_blueprint(usuario_bp, url_prefix='/user')
app.register_blueprint(bairro_bp, url_prefix='/bairro')
app.register_blueprint(jogo_bp, url_prefix='/jogo')

with app.app_context():

    db.create_all()
    print('Banco de dados verificado/criado com sucesso!')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
