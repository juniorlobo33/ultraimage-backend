from flask import Blueprint

user_bp = Blueprint('user', __name__)

@user_bp.route('/test-nome')
def test_nome():
    return {'message': 'Rota nome funcionando'}
