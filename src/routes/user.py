from flask import Blueprint

user_bp = Blueprint('user', __name__)

@user_bp.route('/test-user')
def test_user():
    return 'Rota de user funcionando'