from flask import Blueprint

image_bp = Blueprint('image', __name__)

@image_bp.route('/test-image')
def test_image():
    return 'Rota de image funcionando'
