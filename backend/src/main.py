https://ultraimage-backend-production.up.railway.app/api/auth/check-auth
from flask import Flask
from flask_cors import CORS

from src.routes.user import user_bp
from src.routes.image import image_bp
from src.routes.auth import auth_bp
from src.routes.payment import payment_bp

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["https://ultraimageai.com"])

# Rotas
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(image_bp, url_prefix='/api/image')
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(payment_bp, url_prefix='/api/payment')

# Rota raiz
@app.route('/')
def home():
    return 'API UltraImage rodando com sucesso!'

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)
