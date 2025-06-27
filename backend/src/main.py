import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.routes.image import image_bp
from src.routes.auth import auth_bp
from src.routes.payment import payment_bp

# Cria a app Flask e configura a pasta estática
app = Flask(
    __name__,
    static_folder=os.path.join(os.path.dirname(__file__), 'static'),
    static_url_path=''
)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'changeme')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 
    f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Habilita CORS
CORS(app, supports_credentials=True)

# Inicializa DB e cria tabelas
db.init_app(app)
with app.app_context():
    db.create_all()

# Registra blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(image_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(payment_bp, url_prefix='/api/payment')

# Rota para servir SPA + API
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder = app.static_folder
    if not static_folder:
        return "Static folder not configured", 404

    # Se existir o arquivo estático, serve-o
    file_path = os.path.join(static_folder, path)
    if path and os.path.exists(file_path) and os.path.isfile(file_path):
        return send_from_directory(static_folder, path)

    # Se não for rota de API, serve index.html (SPA fallback)
    if not path.startswith('api/'):
        index_path = os.path.join(static_folder, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder, 'index.html')

    # Rota de API não encontrada
    return "Not found", 404

# Apenas roda o servidor de dev quando executar `python main.py`
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
