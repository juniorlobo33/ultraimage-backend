from flask import Blueprint

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/test-nome')
def test_nome():
    return {'message': 'Rota nome funcionando'}
