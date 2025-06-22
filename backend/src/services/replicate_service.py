import os
import requests
import replicate
from PIL import Image
import io
import base64
import uuid
from datetime import datetime

class ReplicateService:
    def __init__(self):
        """Inicializar o serviço Replicate com a API key"""
        self.api_token = os.environ.get('REPLICATE_API_TOKEN')
        if not self.api_token:
            raise ValueError("REPLICATE_API_TOKEN não encontrado nas variáveis de ambiente")
        
        # Configurar cliente Replicate
        self.client = replicate.Client(api_token=self.api_token)
        
        # Modelos disponíveis
        self.models = {
            'upscale': 'nightmareai/real-esrgan:42fed1c4974146d4d2414e2be2c5277c7fcf05fcc972b6f777b83f18e0b5ee90',
            'enhance': 'tencentarc/gfpgan:9283608cc6b7be6b65a8e44983db012355fde4132009bf99d976b2f0896856a3',
            'colorize': 'cjwbw/bigcolor:9451bfbf652b21a9bccc741e5c7046540faa5586cfa3aa45abc7c6e5c0b5e7b5'
        }
    
    def upscale_image(self, image_data, scale=2, model_type='upscale'):
        """
        Fazer upscale de uma imagem usando Real-ESRGAN
        
        Args:
            image_data: Dados da imagem (bytes ou base64)
            scale: Fator de escala (2, 4, 8)
            model_type: Tipo de modelo a usar
            
        Returns:
            dict: Resultado com URL da imagem processada
        """
        try:
            # Converter image_data para URL ou base64 se necessário
            if isinstance(image_data, bytes):
                # Converter bytes para base64
                image_b64 = base64.b64encode(image_data).decode('utf-8')
                image_url = f"data:image/jpeg;base64,{image_b64}"
            elif isinstance(image_data, str) and image_data.startswith('http'):
                # Já é uma URL
                image_url = image_data
            else:
                # Assumir que é base64
                image_url = f"data:image/jpeg;base64,{image_data}"
            
            # Configurar parâmetros do modelo
            model_name = self.models.get(model_type, self.models['upscale'])
            
            input_params = {
                "image": image_url,
                "scale": scale
            }
            
            # Executar o modelo
            output = self.client.run(model_name, input=input_params)
            
            # O output geralmente é uma URL da imagem processada
            if isinstance(output, list) and len(output) > 0:
                result_url = output[0]
            elif isinstance(output, str):
                result_url = output
            else:
                raise ValueError("Formato de saída inesperado do modelo")
            
            return {
                'success': True,
                'result_url': result_url,
                'model_used': model_name,
                'scale': scale,
                'processed_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'model_used': model_name if 'model_name' in locals() else None
            }
    
    def enhance_image(self, image_data):
        """
        Melhorar qualidade de uma imagem usando GFPGAN
        
        Args:
            image_data: Dados da imagem
            
        Returns:
            dict: Resultado com URL da imagem processada
        """
        return self.upscale_image(image_data, scale=1, model_type='enhance')
    
    def colorize_image(self, image_data):
        """
        Colorir uma imagem em preto e branco
        
        Args:
            image_data: Dados da imagem
            
        Returns:
            dict: Resultado com URL da imagem processada
        """
        try:
            # Converter image_data para URL se necessário
            if isinstance(image_data, bytes):
                image_b64 = base64.b64encode(image_data).decode('utf-8')
                image_url = f"data:image/jpeg;base64,{image_b64}"
            elif isinstance(image_data, str) and image_data.startswith('http'):
                image_url = image_data
            else:
                image_url = f"data:image/jpeg;base64,{image_data}"
            
            model_name = self.models['colorize']
            
            input_params = {
                "image": image_url
            }
            
            output = self.client.run(model_name, input=input_params)
            
            if isinstance(output, list) and len(output) > 0:
                result_url = output[0]
            elif isinstance(output, str):
                result_url = output
            else:
                raise ValueError("Formato de saída inesperado do modelo")
            
            return {
                'success': True,
                'result_url': result_url,
                'model_used': model_name,
                'processed_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def download_result_image(self, result_url):
        """
        Baixar imagem processada da URL de resultado
        
        Args:
            result_url: URL da imagem processada
            
        Returns:
            bytes: Dados da imagem baixada
        """
        try:
            response = requests.get(result_url, timeout=30)
            response.raise_for_status()
            return response.content
            
        except Exception as e:
            raise Exception(f"Erro ao baixar imagem: {str(e)}")
    
    def validate_image(self, image_data, max_size_mb=10):
        """
        Validar se a imagem está dentro dos limites aceitos
        
        Args:
            image_data: Dados da imagem
            max_size_mb: Tamanho máximo em MB
            
        Returns:
            dict: Resultado da validação
        """
        try:
            # Verificar tamanho
            if isinstance(image_data, bytes):
                size_mb = len(image_data) / (1024 * 1024)
            else:
                # Para base64, estimar tamanho
                size_mb = len(image_data) * 0.75 / (1024 * 1024)
            
            if size_mb > max_size_mb:
                return {
                    'valid': False,
                    'error': f'Imagem muito grande: {size_mb:.2f}MB (máximo: {max_size_mb}MB)'
                }
            
            # Verificar se é uma imagem válida
            if isinstance(image_data, bytes):
                try:
                    img = Image.open(io.BytesIO(image_data))
                    img.verify()
                except Exception:
                    return {
                        'valid': False,
                        'error': 'Formato de imagem inválido'
                    }
            
            return {
                'valid': True,
                'size_mb': size_mb
            }
            
        except Exception as e:
            return {
                'valid': False,
                'error': f'Erro na validação: {str(e)}'
            }
    
    def get_available_models(self):
        """
        Retornar lista de modelos disponíveis
        
        Returns:
            dict: Modelos disponíveis
        """
        return {
            'models': self.models,
            'descriptions': {
                'upscale': 'Aumentar resolução da imagem (Real-ESRGAN)',
                'enhance': 'Melhorar qualidade facial (GFPGAN)',
                'colorize': 'Colorir imagem em preto e branco'
            }
        }
    
    def health_check(self):
        """
        Verificar se o serviço está funcionando
        
        Returns:
            dict: Status do serviço
        """
        try:
            # Verificar se a API key está configurada
            if not self.api_token:
                return {
                    'healthy': False,
                    'error': 'API token não configurado'
                }
            
            # Verificar se consegue acessar a API (teste simples)
            # Em produção, você pode fazer uma chamada de teste real
            
            return {
                'healthy': True,
                'api_configured': True,
                'models_available': len(self.models)
            }
            
        except Exception as e:
            return {
                'healthy': False,
                'error': str(e)
            }

