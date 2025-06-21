from flask import Blueprint

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/test-payment')
def test_payment():
    return 'Rota de payment funcionando'