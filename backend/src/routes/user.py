from flask import Blueprint

user_bp = Blueprint('nome', __name__)

@user_bp.route('/test-nome')
def test_nome():
    return {'message': 'Rota nome funcionando'}
