from flask import Blueprint

image_bp = Blueprint('nome', __name__)

@nome_bp.route('/test-nome')
def test_nome():
    return {'message': 'Rota nome funcionando'}
