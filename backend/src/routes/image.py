from flask import Blueprint

image_bp = Blueprint('image', __name__)

@image_bp.route('/test-nome')
def test_nome():
    return {'message': 'Rota nome funcionando'}
