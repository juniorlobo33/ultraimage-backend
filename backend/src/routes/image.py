from flask import Blueprint, jsonify

image_bp = Blueprint('image', __name__)

@image_bp.route('/upload', methods=['POST'])
def upload_image():
    return jsonify({
        'success': True,
        'jobId': 123,  # ID fixo para teste
        'message': 'Upload realizado com sucesso!'
    }), 200

@image_bp.route('/status/<int:job_id>', methods=['GET'])
def get_processing_status(job_id):
    return jsonify({
        'jobId': job_id,
        'status': 'completed',
        'result': {
            'downloadUrl': f'/api/image/download/{job_id}',
            'originalFilename': 'test_image.jpg'
        }
    }), 200

@image_bp.route('/download/<int:job_id>', methods=['GET'])
def download_result(job_id):
    return jsonify({
        'message': f'Download simulado para job {job_id}',
        'jobId': job_id
    }), 200

@image_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'image-processing-minimal'
    }), 200

