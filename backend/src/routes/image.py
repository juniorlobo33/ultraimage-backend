from flask import Blueprint, request, jsonify, current_app, send_file
from werkzeug.utils import secure_filename
import os
import uuid
import requests
import replicate
from datetime import datetime

image_bp = Blueprint('image', __name__)

# Configurações
UPLOAD_FOLDER = '/tmp/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Criar pasta de upload
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_size(file):
    file.seek(0, 2)
    size = file.tell()
    file.seek(0)
    return size

# Armazenamento em memória para jobs (temporário)
jobs_storage = {}

@image_bp.route('/upload', methods=['POST'])
def upload_image():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Tipo de arquivo não suportado'}), 400
        
        file_size = get_file_size(file)
        if file_size > MAX_FILE_SIZE:
            return jsonify({'error': 'Arquivo muito grande. Máximo 10MB'}), 400
        
        # Salvar arquivo
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        file.save(file_path)
        
        # Gerar job ID
        job_id = len(jobs_storage) + 1
        
        # Armazenar job
        jobs_storage[job_id] = {
            'status': 'processing',
            'input_path': file_path,
            'output_path': None,
            'original_filename': file.filename,
            'created_at': datetime.utcnow().isoformat()
        }
        
        # Processar com Replicate em background
        try:
            process_with_replicate(job_id, file_path)
        except Exception as e:
            current_app.logger.error(f"Erro no processamento: {str(e)}")
            jobs_storage[job_id]['status'] = 'failed'
            jobs_storage[job_id]['error'] = str(e)
        
        return jsonify({
            'success': True,
            'jobId': job_id,
            'message': 'Upload realizado! Processando com IA...'
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Erro no upload: {str(e)}")
        return jsonify({'error': f'Erro no upload: {str(e)}'}), 500

def process_with_replicate(job_id, input_path):
    """Processar imagem com Replicate"""
    try:
        # Configurar Replicate
        replicate_token = os.environ.get('REPLICATE_API_TOKEN')
        if not replicate_token:
            raise Exception("Token Replicate não configurado")
        
        # Abrir arquivo
        with open(input_path, 'rb') as image_file:
            # Executar modelo Real-ESRGAN
            output = replicate.run(
                "nightmareai/real-esrgan:42fed1c4974146d4d2414e2be2c5277c7fcf05fcc3a73abf41610695738c1d7b",
                input={
                    "image": image_file,
                    "scale": 4,  # 4x upscaling
                    "face_enhance": False
                }
            )
            
            if output:
                # Baixar resultado
                response = requests.get(output, timeout=60)
                response.raise_for_status()
                
                # Salvar resultado
                output_filename = f"upscaled_{uuid.uuid4()}.png"
                output_path = os.path.join(UPLOAD_FOLDER, output_filename)
                
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                
                # Atualizar job
                jobs_storage[job_id]['status'] = 'completed'
                jobs_storage[job_id]['output_path'] = output_path
                jobs_storage[job_id]['completed_at'] = datetime.utcnow().isoformat()
                
                current_app.logger.info(f"Processamento concluído para job {job_id}")
            else:
                raise Exception("Replicate retornou resultado vazio")
                
    except Exception as e:
        current_app.logger.error(f"Erro no processamento Replicate: {str(e)}")
        jobs_storage[job_id]['status'] = 'failed'
        jobs_storage[job_id]['error'] = str(e)

@image_bp.route('/status/<int:job_id>', methods=['GET'])
def get_processing_status(job_id):
    try:
        if job_id not in jobs_storage:
            return jsonify({'error': 'Job não encontrado'}), 404
        
        job = jobs_storage[job_id]
        
        response_data = {
            'jobId': job_id,
            'status': job['status'],
            'created_at': job.get('created_at')
        }
        
        if job['status'] == 'completed' and job.get('output_path'):
            response_data['result'] = {
                'downloadUrl': f'/api/image/download/{job_id}',
                'originalFilename': job['original_filename']
            }
        elif job['status'] == 'failed':
            response_data['error'] = job.get('error', 'Erro desconhecido')
        
        return jsonify(response_data), 200
        
    except Exception as e:
        current_app.logger.error(f"Erro ao verificar status: {str(e)}")
        return jsonify({'error': 'Erro interno'}), 500

@image_bp.route('/download/<int:job_id>', methods=['GET'])
def download_result(job_id):
    try:
        if job_id not in jobs_storage:
            return jsonify({'error': 'Job não encontrado'}), 404
        
        job = jobs_storage[job_id]
        
        if job['status'] != 'completed' or not job.get('output_path'):
            return jsonify({'error': 'Processamento não concluído'}), 400
        
        output_path = job['output_path']
        if not os.path.exists(output_path):
            return jsonify({'error': 'Arquivo não encontrado'}), 404
        
        return send_file(
            output_path,
            as_attachment=True,
            download_name=f"upscaled_{job['original_filename']}"
        )
        
    except Exception as e:
        current_app.logger.error(f"Erro no download: {str(e)}")
        return jsonify({'error': 'Erro no download'}), 500

@image_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'image-processing-real',
        'replicate_configured': bool(os.environ.get('REPLICATE_API_TOKEN'))
    }), 200

