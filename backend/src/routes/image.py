from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime
from src.models.user import db, ProcessingJob
from src.services.replicate_service import process_image_with_replicate
import threading

image_bp = Blueprint('image', __name__)

# Configurações de upload
UPLOAD_FOLDER = '/tmp/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Criar pasta de upload se não existir
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_size(file):
    file.seek(0, 2)  # Ir para o final do arquivo
    size = file.tell()
    file.seek(0)  # Voltar para o início
    return size

@image_bp.route('/upload', methods=['POST'])
def upload_image():
    try:
        # Verificar se há arquivo na requisição
        if 'image' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['image']
        
        # Verificar se arquivo foi selecionado
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        # Verificar tipo de arquivo
        if not allowed_file(file.filename):
            return jsonify({'error': 'Tipo de arquivo não suportado. Use JPG, PNG ou WebP.'}), 400
        
        # Verificar tamanho do arquivo
        file_size = get_file_size(file)
        if file_size > MAX_FILE_SIZE:
            return jsonify({'error': 'Arquivo muito grande. Máximo 10MB.'}), 400
        
        # Gerar nome único para o arquivo
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        
        # Salvar arquivo
        file.save(file_path)
        
        # Criar registro no banco de dados
        job = ProcessingJob(
            user_id=1,  # TODO: Pegar do usuário logado
            status='uploaded',
            input_path=file_path,
            original_filename=file.filename,
            file_size=file_size,
            created_at=datetime.utcnow()
        )
        
        db.session.add(job)
        db.session.commit()
        
        # Iniciar processamento em background
        thread = threading.Thread(
            target=process_image_background,
            args=(job.id, file_path)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'jobId': job.id,
            'message': 'Upload realizado com sucesso. Processamento iniciado.'
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Erro no upload: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@image_bp.route('/status/<int:job_id>', methods=['GET'])
def get_processing_status(job_id):
    try:
        job = ProcessingJob.query.get(job_id)
        
        if not job:
            return jsonify({'error': 'Job não encontrado'}), 404
        
        response_data = {
            'jobId': job.id,
            'status': job.status,
            'created_at': job.created_at.isoformat() if job.created_at else None,
            'completed_at': job.completed_at.isoformat() if job.completed_at else None
        }
        
        # Se processamento concluído, incluir URL de download
        if job.status == 'completed' and job.output_path:
            response_data['result'] = {
                'downloadUrl': f'/api/image/download/{job.id}',
                'originalFilename': job.original_filename
            }
        
        # Se erro, incluir mensagem
        if job.status == 'failed' and job.error_message:
            response_data['error'] = job.error_message
        
        return jsonify(response_data), 200
        
    except Exception as e:
        current_app.logger.error(f"Erro ao verificar status: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@image_bp.route('/download/<int:job_id>', methods=['GET'])
def download_result(job_id):
    try:
        job = ProcessingJob.query.get(job_id)
        
        if not job:
            return jsonify({'error': 'Job não encontrado'}), 404
        
        if job.status != 'completed' or not job.output_path:
            return jsonify({'error': 'Processamento não concluído'}), 400
        
        # Verificar se arquivo existe
        if not os.path.exists(job.output_path):
            return jsonify({'error': 'Arquivo não encontrado'}), 404
        
        # Retornar arquivo para download
        from flask import send_file
        return send_file(
            job.output_path,
            as_attachment=True,
            download_name=f"upscaled_{job.original_filename}"
        )
        
    except Exception as e:
        current_app.logger.error(f"Erro no download: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

def process_image_background(job_id, input_path):
    """Processar imagem em background usando Replicate"""
    try:
        # Atualizar status para processando
        job = ProcessingJob.query.get(job_id)
        job.status = 'processing'
        db.session.commit()
        
        # Processar com Replicate
        output_url = process_image_with_replicate(input_path)
        
        if output_url:
            # Download do resultado
            import requests
            response = requests.get(output_url)
            
            if response.status_code == 200:
                # Salvar resultado
                output_filename = f"result_{uuid.uuid4()}.png"
                output_path = os.path.join(UPLOAD_FOLDER, output_filename)
                
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                
                # Atualizar job como concluído
                job.status = 'completed'
                job.output_path = output_path
                job.completed_at = datetime.utcnow()
                db.session.commit()
            else:
                raise Exception("Erro ao baixar resultado do Replicate")
        else:
            raise Exception("Erro no processamento com Replicate")
            
    except Exception as e:
        # Atualizar job como falhou
        job = ProcessingJob.query.get(job_id)
        job.status = 'failed'
        job.error_message = str(e)
        job.completed_at = datetime.utcnow()
        db.session.commit()
        
        current_app.logger.error(f"Erro no processamento background: {str(e)}")

@image_bp.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificar se o serviço está funcionando"""
    return jsonify({
        'status': 'healthy',
        'service': 'image-processing',
        'timestamp': datetime.utcnow().isoformat()
    }), 200

