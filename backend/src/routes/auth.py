from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/test-nome')
def test_nome():
    return {'message': 'Rota nome funcionando'}
