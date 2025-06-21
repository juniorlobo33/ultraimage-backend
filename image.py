from flask import Blueprint, request, jsonify, send_file
import os
import uuid
from werkzeug.utils import secure_filename
from src.services.replicate_service import ReplicateService

image_bp = Blueprint('image', __name__)

UPLOAD_FOLDER = '/tmp/uploads'
PROCESSED_FOLDER = '/tmp/processed'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Criar pastas se não existirem
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Inicializar serviço Replicate
replicate_service = ReplicateService()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@image_bp.route('/upload', methods=['POST'])
def upload_image():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'Nenhuma imagem foi enviada'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        if file and allowed_file(file.filename):
            # Gerar nome único para o arquivo
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
            
            # Salvar arquivo
            file.save(filepath)
            
            return jsonify({
                'message': 'Upload realizado com sucesso',
                'filename': unique_filename,
                'filepath': filepath
            }), 200
        else:
            return jsonify({'error': 'Tipo de arquivo não permitido'}), 400
            
    except Exception as e:
        return jsonify({'error': f'Erro no upload: {str(e)}'}), 500

@image_bp.route('/process', methods=['POST'])
def process_image():
    try:
        data = request.get_json()
        
        if not data or 'filename' not in data:
            return jsonify({'error': 'Nome do arquivo não fornecido'}), 400
        
        filename = data['filename']
        scale = data.get('scale', 2)  # Padrão: 2x
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        if not os.path.exists(filepath):
            return jsonify({'error': 'Arquivo não encontrado'}), 404
        
        # Processar imagem com Replicate
        result = replicate_service.upscale_image(filepath, scale)
        
        if result['success']:
            job_id = str(uuid.uuid4())
            
            # Simular processamento assíncrono
            # Em produção, você salvaria o job_id e o resultado no banco de dados
            
            return jsonify({
                'message': 'Processamento iniciado',
                'status': 'processing',
                'job_id': job_id,
                'scale': scale
            }), 200
        else:
            return jsonify({'error': result['error']}), 500
        
    except Exception as e:
        return jsonify({'error': f'Erro no processamento: {str(e)}'}), 500

@image_bp.route('/status/<job_id>', methods=['GET'])
def get_status(job_id):
    try:
        # Em produção, você consultaria o banco de dados pelo job_id
        # e verificaria o status no Replicate se necessário
        
        # Simulação de status concluído
        return jsonify({
            'job_id': job_id,
            'status': 'completed',
            'progress': 100,
            'result_url': f'/api/download/{job_id}',
            'output_url': 'https://example.com/processed_image.png'
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro ao verificar status: {str(e)}'}), 500

@image_bp.route('/download/<job_id>', methods=['GET'])
def download_result(job_id):
    try:
        # Em produção, você recuperaria o arquivo processado
        # baseado no job_id do banco de dados
        
        # Simulação de download
        return jsonify({
            'message': 'Download simulado',
            'job_id': job_id,
            'download_url': f'https://example.com/download/{job_id}.png'
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro no download: {str(e)}'}), 500

@image_bp.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificar se a API está funcionando"""
    return jsonify({
        'status': 'healthy',
        'service': 'Image Processing API',
        'replicate_configured': replicate_service.api_token is not None
    }), 200

