import os
import io
import base64
import time
import uuid
from flask import Blueprint, request, jsonify, send_file
from PIL import Image
import replicate
import requests

image_bp = Blueprint('image', __name__)

# Max pixel limit for Replicate GPU (approx 4 million pixels)
MAX_PIXELS = 4000000

@image_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "service": "image-processing",
        "status": "healthy",
        "timestamp": time.time()
    })

@image_bp.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "Nenhuma imagem enviada"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "Nenhum arquivo selecionado"}), 400

    if not file:
        return jsonify({"error": "Arquivo inválido"}), 400

    try:
        # Read image and convert to PIL Image
        img_bytes = file.read()
        original_image = Image.open(io.BytesIO(img_bytes)).convert("RGB")

        # Get parameters from request (with defaults)
        scale = int(request.form.get('scale', 2)) # Default to 2x for stability
        face_enhance = request.form.get('face_enhance', 'false').lower() == 'true'
        denoise = float(request.form.get('denoise', 0.5))

        # Check image dimensions and resize if necessary
        width, height = original_image.size
        current_pixels = width * height

        if current_pixels > MAX_PIXELS:
            # Calculate new dimensions to fit within MAX_PIXELS while maintaining aspect ratio
            ratio = (MAX_PIXELS / current_pixels)**0.5
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            original_image = original_image.resize((new_width, new_height), Image.LANCZOS)
            print(f"Imagem redimensionada de {width}x{height} para {new_width}x{new_height}")

        # Save image to a temporary buffer for Replicate
        temp_input_buffer = io.BytesIO()
        original_image.save(temp_input_buffer, format="PNG") # Replicate often prefers PNG
        temp_input_buffer.seek(0)

        # Call Replicate API
        print(f"Chamando Replicate com scale={scale}, face_enhance={face_enhance}, denoise={denoise}")
        output = replicate.run(
            "stability-ai/real-esrgan:3556565136eab5003edff6c0b7677325617e006a390097793aef073bc739674b",
            input={
                "image": temp_input_buffer,
                "scale": scale,
                "face_enhance": face_enhance,
                "denoise": denoise
            }
        )
        print(f"Replicate output: {output}")

        if not output:
            raise Exception("Replicate retornou uma saída vazia.")

        # Download the processed image
        processed_image_url = output
        response = requests.get(processed_image_url)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

        processed_image_bytes = io.BytesIO(response.content)
        processed_image_bytes.seek(0)

        # Generate a unique filename for download
        unique_filename = f"enhanced_{uuid.uuid4().hex}.png"

        # Store the processed image in a temporary location or session for download
        # For simplicity, we'll return it directly as base64 for now,
        # or you can save it to a temp folder and provide a download link.
        
        # Encode processed image to base64
        encoded_image = base64.b64encode(processed_image_bytes.getvalue()).decode('utf-8')

        return jsonify({
            "message": "Imagem processada com sucesso!",
            "jobId": "processed_image", # Placeholder jobId
            "imageUrl": f"data:image/png;base64,{encoded_image}"
        }), 200

    except replicate.exceptions.ReplicateError as e:
        print(f"Erro do Replicate: {e}")
        return jsonify({"error": f"Erro no processamento da IA: {str(e)}"}), 500
    except requests.exceptions.RequestException as e:
        print(f"
