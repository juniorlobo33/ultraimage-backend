from flask import Blueprint, jsonify

image_bp = Blueprint('image', __name__)

@image_bp.route('/upload', methods=['POST'])
def upload_image():
    return jsonify({
        'success': True,
        'message': 'Endpoint funcionando!'
    }), 200

@image_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'image-processing-minimal'
    }), 200

