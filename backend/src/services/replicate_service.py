import replicate
import os
import requests
from flask import current_app

def process_image_with_replicate(input_image_path):
    """
    Processa uma imagem usando o modelo Real-ESRGAN no Replicate
    
    Args:
        input_image_path (str): Caminho para a imagem de entrada
        
    Returns:
        str: URL da imagem processada ou None se houver erro
    """
    try:
        # Verificar se o token está configurado
        api_token = os.environ.get('REPLICATE_API_TOKEN')
        if not api_token:
            current_app.logger.error("REPLICATE_API_TOKEN não configurado")
            return None
        
        # Configurar cliente Replicate
        replicate_client = replicate.Client(api_token=api_token)
        
        # Abrir e ler a imagem
        with open(input_image_path, 'rb') as image_file:
            # Executar o modelo Real-ESRGAN
            output = replicate_client.run(
                "nightmareai/real-esrgan:42fed1c4974146d4d2414e2be2c5277c7fcf05fcc3a73abf41610695738c1d7b",
                input={
                    "image": image_file,
                    "scale": 4,  # Fator de escala (2x, 4x, 8x)
                    "face_enhance": False  # Melhoramento específico para rostos
                }
            )
            
            # O output é uma URL da imagem processada
            if output:
                current_app.logger.info(f"Processamento concluído: {output}")
                return output
            else:
                current_app.logger.error("Replicate retornou output vazio")
                return None
                
    except Exception as e:
        current_app.logger.error(f"Erro no processamento Replicate: {str(e)}")
        return None

def process_image_async(input_image_path):
    """
    Inicia processamento assíncrono no Replicate
    
    Args:
        input_image_path (str): Caminho para a imagem de entrada
        
    Returns:
        str: ID da predição para monitoramento ou None se houver erro
    """
    try:
        # Verificar se o token está configurado
        api_token = os.environ.get('REPLICATE_API_TOKEN')
        if not api_token:
            current_app.logger.error("REPLICATE_API_TOKEN não configurado")
            return None
        
        # Configurar cliente Replicate
        replicate_client = replicate.Client(api_token=api_token)
        
        # Abrir e ler a imagem
        with open(input_image_path, 'rb') as image_file:
            # Criar predição assíncrona
            prediction = replicate_client.predictions.create(
                version="42fed1c4974146d4d2414e2be2c5277c7fcf05fcc3a73abf41610695738c1d7b",
                input={
                    "image": image_file,
                    "scale": 4,
                    "face_enhance": False
                }
            )
            
            current_app.logger.info(f"Predição criada: {prediction.id}")
            return prediction.id
                
    except Exception as e:
        current_app.logger.error(f"Erro ao criar predição: {str(e)}")
        return None

def get_prediction_status(prediction_id):
    """
    Verifica o status de uma predição
    
    Args:
        prediction_id (str): ID da predição
        
    Returns:
        dict: Status e resultado da predição
    """
    try:
        api_token = os.environ.get('REPLICATE_API_TOKEN')
        if not api_token:
            return {'status': 'error', 'error': 'Token não configurado'}
        
        replicate_client = replicate.Client(api_token=api_token)
        prediction = replicate_client.predictions.get(prediction_id)
        
        return {
            'status': prediction.status,
            'output': prediction.output,
            'error': prediction.error
        }
        
    except Exception as e:
        current_app.logger.error(f"Erro ao verificar predição: {str(e)}")
        return {'status': 'error', 'error': str(e)}

def download_image(url, output_path):
    """
    Baixa uma imagem de uma URL
    
    Args:
        url (str): URL da imagem
        output_path (str): Caminho onde salvar a imagem
        
    Returns:
        bool: True se sucesso, False se erro
    """
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        current_app.logger.info(f"Imagem baixada: {output_path}")
        return True
        
    except Exception as e:
        current_app.logger.error(f"Erro ao baixar imagem: {str(e)}")
        return False

def health_check():
    """
    Verifica se o serviço Replicate está acessível
    
    Returns:
        dict: Status do serviço
    """
    try:
        api_token = os.environ.get('REPLICATE_API_TOKEN')
        if not api_token:
            return {'status': 'error', 'message': 'Token não configurado'}
        
        # Tentar listar modelos para verificar conectividade
        replicate_client = replicate.Client(api_token=api_token)
        
        # Fazer uma requisição simples para testar
        models = list(replicate_client.models.list()[:1])
        
        return {'status': 'healthy', 'message': 'Replicate acessível'}
        
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

