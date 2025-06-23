import os
import io
import base64
import time
from flask import Blueprint, request, jsonify, send_file
from PIL import Image
import replicate
import tempfile
import numpy as np

image_bp = Blueprint('image', __name__)

# Configurações do Replicate
REPLICATE_MODEL = "nightmareai/real-esrgan:42fed1c4974146d4d2414e2be2c5277c7fdb0ef3c0669c590548137b9ed9f221"
MAX_PIXELS = 4 * 1024 * 1024 # Limite de 4 milhões de pixels para o GPU

@image_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"service": "image-processing", "status": "healthy", "timestamp": time.time()})

@image_bp.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "Nenhuma imagem fornecida"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "Nenhum arquivo selecionado"}), 400

    if file:
        try:
            # Ler a imagem
            img = Image.open(io.BytesIO(file.read()))
            original_format = img.format

            # Obter parâmetros do frontend
            scale = int(request.form.get('scale', 2)) # Padrão 2x
            face_enhance = request.form.get('face_enhance', 'false').lower() == 'true'

            # Redimensionar se a imagem for muito grande
            width, height = img.size
            current_pixels = width * height
            if current_pixels > MAX_PIXELS:
                ratio = (MAX_PIXELS / current_pixels)**0.5
                new_width = int(width * ratio)
                new_height = int(height * ratio)
                img = img.resize((new_width, new_height), Image.LANCZOS)
                print(f"Imagem redimensionada de {width}x{height} para {new_width}x{new_height}")

            # Converter para RGB se necessário (Replicate prefere RGB)
            if img.mode != 'RGB':
                img = img.convert('RGB')

            # Salvar imagem temporariamente para o Replicate
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{original_format.lower()}") as temp_input_file:
                img.save(temp_input_file.name, format=original_format)
                temp_input_file_path = temp_input_file.name

            print(f"Iniciando processamento Replicate para {temp_input_file_path} com scale={scale}, face_enhance={face_enhance}")

            # Chamar o modelo Replicate
            output_url = replicate.run(
                REPLICATE_MODEL,
                input={
                    "image": open(temp_input_file_path, "rb"),
                    "scale": scale,
                    "face_enhance": face_enhance
                }
            )
            print(f"Processamento Replicate concluído. Output URL: {output_url}")

            # Baixar a imagem processada
            import requests
            response = requests.get(output_url)
            response.raise_for_status() # Levanta um erro para status HTTP ruins

            # Salvar a imagem processada temporariamente
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{original_format.lower()}") as temp_output_file:
                temp_output_file.write(response.content)
                temp_output_file_path = temp_output_file.name

            # Ler a imagem processada para base64
            with open(temp_output_file_path, "rb") as f:
                encoded_image = base64.b64encode(f.read()).decode('utf-8')

            # Limpar arquivos temporários
            os.unlink(temp_input_file_path)
            os.unlink(temp_output_file_path)

            return jsonify({
                "message": "Upload e processamento concluídos!",
                "processed_image": encoded_image,
                "jobId": "processed_image_id" # ID simulado
            }), 200

        except replicate.exceptions.ReplicateError as e:
            print(f"Erro do Replicate: {e}")
            return jsonify({"error": f"Erro no processamento Replicate: {e}"}), 500
        except requests.exceptions.RequestException as e:
            print(f"Erro ao baixar imagem do Replicate: {e}")
            return jsonify({"error": f"Erro ao baixar imagem processada: {e}"}), 500
        except Exception as e:
            print(f"Erro interno no servidor: {e}")
            return jsonify({"error": f"Erro interno no servidor: {e}"}), 500

    return jsonify({"error": "Erro desconhecido"}), 500

@image_bp.route('/status/<job_id>', methods=['GET'])
def get_status(job_id):
    # Como o processamento é síncrono, sempre retorna 'completed'
    return jsonify({"status": "completed", "jobId": job_id}), 200

@image_bp.route('/download/<job_id>', methods=['GET'])
def download_image(job_id):
    # Esta rota não será usada diretamente pelo frontend com o fluxo atual
    # O frontend recebe a imagem base64 diretamente no upload
    return jsonify({"error": "Download direto não suportado para este fluxo"}), 400

