import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask
from flask_cors import CORS

from src.routes.user import user_bp
from src.routes.image import image_bp
from src.routes.auth import auth_bp
from src.routes.payment import payment_bp

app = Flask(__name__)

app.config['SECRET_KEY'] = 'sua_secret_key'

CORS(app, supports_credentials=True)

# Registrando as rotas
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(image_bp, url_prefix='/api/image')
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(payment_bp, url_prefix='/api/payment')

@app.route('/')
def home():
    return 'API UltraImage está rodando!'

if __name__ == '__main__':
    app.run(debug=True)
