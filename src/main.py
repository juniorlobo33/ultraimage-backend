import os
import sys

# Adiciona o diretório atual no path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS

# Importando as rotas
from src.routes.user import user_bp
from src.routes.image import image_bp
from src.routes.auth import auth_bp
from src.routes.payment import payment_bp

# Inicializando a aplicação Flask
app = Flask(__name__)

# Configuração
app.config['SECRET_KEY'] = 'sua_secret_key'

# Habilita CORS
CORS(app, supports_credentials=True)

# Registrando as rotas
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(image_bp, url_prefix='/api/image')
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(payment_bp, url_prefix='/api/payment')

# Rota principal para teste
@app.route('/')
def home():
    return '🚀 API UltraImage está rodando com sucesso!'

# Executa localmente
if __name__ == '__main__':
    app.run(debug=True)

# Para Gunicorn encontrar o app
app = app
