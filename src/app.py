from flask import Flask
from database import db
from flask_cors import CORS
from routes.user_routes import usuario_bp
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

CORS(
    app,
    resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
        }
    },
)

db.init_app(app)

app.register_blueprint(usuario_bp)

with app.app_context():
    db.create_all()
    print("Banco de dados verificado/criado com sucesso!")

if __name__ == "__main__":
    app.run(debug=True)
