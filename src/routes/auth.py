from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/test-auth')
def test_auth():
    return 'Rota de auth funcionando'