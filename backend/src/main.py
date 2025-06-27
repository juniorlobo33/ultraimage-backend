import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.routes.image import image_bp
from src.routes.auth import auth_bp
from src.routes.payment import payment_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

app.config['SECRET_KEY'] = 'asd#df$G5vgas6f$5$WGT'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app, supports_credentials=True, origins=["https://ultraimageai.com"])

# Registrar blueprints da API ANTES das rotas catch-all
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(image_bp, url_prefix='/api/image')
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(payment_bp, url_prefix='/api/payment')

db.init_app(app)

with app.app_context():
    db.create_all()

# Rota específica para a raiz
@app.route('/')
def serve_index():
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404
    
    index_path = os.path.join(static_folder_path, 'index.html')
    if os.path.exists(index_path):
        return send_from_directory(static_folder_path, 'index.html')
    else:
        return "index.html not found", 404

# Rota catch-all APENAS para arquivos estáticos e páginas do frontend
# IMPORTANTE: Esta rota deve vir DEPOIS dos blueprints da API
@app.route('/<path:path>')
def serve_static_or_spa(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    # Se o arquivo existe, serve o arquivo estático
    file_path = os.path.join(static_folder_path, path)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return send_from_directory(static_folder_path, path)
    
    # Se não é uma rota da API, serve o index.html (SPA)
    if not path.startswith('api/'):
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
    
    # Se é uma rota da API que não foi encontrada, retorna 404
    return "Not found", 404

 if __name__ == '__main__':
-    app.run(host='0.0.0.0', port=5000, debug=True)
+    # Em produção usamos Gunicorn, não o servidor de dev Flask
+    # app.run(host='0.0.0.0', port=5000, debug=True)

