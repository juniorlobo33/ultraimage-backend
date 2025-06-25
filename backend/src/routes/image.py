import os
import io
import base64
import time
from flask import Blueprint, request, jsonify, send_file
from PIL import Image
import replicate
import tempfile
import numpy as np # Certifique-se de que numpy está importado
import requests # <--- IMPORTANTE: GARANTA QUE ESTA LINHA ESTÁ AQUI NO TOPO!

image_bp = Blueprint('image', __name__)

# Configurações do Replicate
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

# Definir um limite máximo de pixels para evitar erros de memória na GPU do Replicate
# O limite de 2096784 pixels é para o modelo Real-ESRGAN.
MAX_PIXELS = 2000000 # Um pouco abaixo do limite para ter margem de segurança

@image_bp.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "Nenhuma imagem fornecida"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "Nenhum arquivo selecionado"}), 400

    try:
        # Ler a imagem e converter para RGB
        img = Image.open(io.BytesIO(file.read())).convert("RGB")
        original_width, original_height = img.size
        print(f"Dimensões originais da imagem: {original_width}x{original_height} pixels")

        # Redimensionar se exceder o MAX_PIXELS
        if original_width * original_height > MAX_PIXELS:
            ratio = (MAX_PIXELS / (original_width * original_height))**0.5
            new_width = int(original_width * ratio)
            new_height = int(original_height * ratio)
            img = img.resize((new_width, new_height), Image.LANCZOS)
            print(f"Imagem redimensionada para: {new_width}x{new_height} pixels (total: {new_width * new_height} pixels)")
        else:
            print(f"Imagem dentro do limite de pixels. Total: {original_width * original_height} pixels")

        # Salvar a imagem redimensionada em um buffer para enviar ao Replicate
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        # Parâmetros de regulagem do frontend
        scale = request.form.get('scale', type=int, default=2)
        face_enhance = request.form.get('face_enhance', type=bool, default=False)

        print(f"Parâmetros recebidos do frontend: scale={scale}, face_enhance={face_enhance}")

        # Salvar temporariamente a imagem para o Replicate
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_img_file:
            temp_img_file.write(img_byte_arr)
            temp_img_path = temp_img_file.name

        print(f"Imagem temporária criada em: {temp_img_path}")

        # Chamar a API do Replicate
        print("Iniciando processamento Replicate...")
        output = replicate.run(
            "nightmareai/real-esrgan:42fed1c4974146d4d2414e2be2c5277c7fdb0ef3c0669c590548134787689c5299b",
            input={
                "image": open(temp_img_path, "rb"),
                "scale": scale,
                "face_enhance": face_enhance,
            }
        )
        output_url = output

        print(f"Processamento Replicate concluído. Output URL: {output_url}")

        # Remover o arquivo temporário
        os.unlink(temp_img_path)

        # Baixar a imagem processada
        response = requests.get(output_url)
        response.raise_for_status() # Levanta um erro para status HTTP ruins (4xx ou 5xx)

        # Retornar a imagem como base64
        encoded_image = base64.b64encode(response.content).decode('utf-8')
        return jsonify({"image": encoded_image})

    except replicate.exceptions.ModelError as e:
        print(f"Erro do Replicate (ModelError): {e}")
        # Captura o erro específico de modelo do Replicate
        return jsonify({"error": f"Erro no processamento da imagem: {e}. Por favor, tente com uma imagem menor ou de menor resolução."}), 400
    except requests.exceptions.RequestException as e:
        print(f"Erro de requisição HTTP: {e}")
        # Captura erros de rede ou HTTP ao baixar a imagem do Replicate
        return jsonify({"error": f"Erro ao baixar a imagem processada: {e}"}), 500
    except Exception as e:
        print(f"Erro inesperado no upload: {e}")
        # Captura qualquer outro erro inesperado
        return jsonify({"error": f"Ocorreu um erro inesperado: {e}"}), 500

