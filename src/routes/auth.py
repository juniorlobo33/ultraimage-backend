from flask import Blueprint

auth.py = Blueprint('user', __name__)

@user_bp.route('/test-user')
def test_user():
    return "User route funcionando!"
