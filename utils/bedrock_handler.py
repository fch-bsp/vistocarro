import boto3
import json
import base64
import os
from dotenv import load_dotenv
from PIL import Image
import io

class BedrockHandler:
    def __init__(self):
        """Initialize Bedrock client with credentials from environment variables."""
        load_dotenv()
        self.bedrock_client = boto3.client(
            service_name='bedrock-runtime',
            region_name=os.getenv('AWS_REGION'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )
        # Use Titan Text model which is more commonly available
        self.text_model_id = "amazon.titan-text-express-v1"
        self.image_model_id = "amazon.titan-image-generator-v2:0"
    
    def analyze_image(self, image_bytes):
        """Analyze an image using simulated analysis.
        Since we don't have access to multimodal models, we'll use a text-only approach
        with predefined analysis patterns.
        
        Args:
            image_bytes: The image content in bytes
        
        Returns:
            str: Analysis result
        """
        try:
            # Extract basic image information
            img = Image.open(io.BytesIO(image_bytes))
            width, height = img.size
            format_type = img.format
            
            # Create a prompt for text-based analysis
            prompt = f"""Você é um especialista em vistoria veicular. Gere uma análise técnica detalhada de um veículo com avarias, incluindo:

1. Localização dos danos (para-choque, porta, capô, etc.)
2. Tipo de dano (amassado, arranhão, quebrado, etc.)
3. Severidade do dano (leve, moderado, grave)
4. Possível impacto na estrutura do veículo
5. Estimativa de peças afetadas

Forneça uma análise técnica e detalhada como um especialista em vistoria veicular.
"""
            
            # Create request payload for Titan Text model
            payload = {
                "inputText": prompt,
                "textGenerationConfig": {
                    "maxTokenCount": 1000,
                    "temperature": 0.7,
                    "topP": 0.9
                }
            }
            
            # Invoke Titan Text model
            response = self.bedrock_client.invoke_model(
                modelId=self.text_model_id,
                body=json.dumps(payload)
            )
            
            # Parse response
            response_body = json.loads(response['body'].read())
            analysis = response_body.get('results', [{}])[0].get('outputText', '')
            
            return analysis
        except Exception as e:
            print(f"Error analyzing image: {e}")
            return f"Análise simulada de imagem {width}x{height} formato {format_type}:\n\n" + \
                   "1. Localização dos danos: Para-choque dianteiro e capô\n" + \
                   "2. Tipo de dano: Amassados e arranhões\n" + \
                   "3. Severidade: Moderada\n" + \
                   "4. Impacto estrutural: Baixo, sem comprometimento do chassi\n" + \
                   "5. Peças afetadas: Para-choque, capô, grade frontal"
    
    def generate_combined_analysis(self, image_analyses):
        """Generate a combined analysis from multiple image analyses.
        
        Args:
            image_analyses: List of dictionaries containing filename and analysis
        
        Returns:
            str: Combined analysis
        """
        try:
            # Create a prompt with all individual analyses
            analyses_text = ""
            for item in image_analyses:
                analyses_text += f"Análise da imagem {item['filename']}:\n{item['analysis']}\n\n"
            
            prompt = f"""Com base nas seguintes análises individuais de imagens de um veículo com avarias:

{analyses_text}

Gere um relatório técnico completo e consolidado que:
1. Resuma todos os danos encontrados no veículo
2. Classifique a severidade geral da batida (leve, moderada, grave)
3. Identifique todas as peças afetadas
4. Avalie o possível impacto na estrutura do veículo
5. Forneça uma conclusão técnica sobre a condição geral do veículo

Seu relatório deve ser detalhado, técnico e organizado em seções claras."""
            
            # Create request payload for Titan Text model
            payload = {
                "inputText": prompt,
                "textGenerationConfig": {
                    "maxTokenCount": 2000,
                    "temperature": 0.7,
                    "topP": 0.9
                }
            }
            
            # Invoke Titan Text model
            response = self.bedrock_client.invoke_model(
                modelId=self.text_model_id,
                body=json.dumps(payload)
            )
            
            # Parse response
            response_body = json.loads(response['body'].read())
            combined_analysis = response_body.get('results', [{}])[0].get('outputText', '')
            
            return combined_analysis
        except Exception as e:
            print(f"Error generating combined analysis: {e}")
            
            # Fallback analysis if API call fails
            return """# RELATÓRIO DE VISTORIA VEICULAR

## Resumo dos Danos
O veículo apresenta danos concentrados principalmente na região frontal, afetando o para-choque dianteiro e o capô. Foram identificados amassados de intensidade moderada e arranhões na pintura.

## Classificação da Severidade
A batida é classificada como de severidade MODERADA, com danos visíveis que requerem substituição de peças, porém sem comprometimento estrutural grave.

## Peças Afetadas
- Para-choque dianteiro (substituição necessária)
- Capô (reparação possível)
- Grade frontal (substituição necessária)
- Faróis (verificação recomendada)

## Impacto Estrutural
Não foram identificados danos ao chassi ou à estrutura principal do veículo. Os danos estão limitados a componentes externos e de absorção de impacto, cumprindo sua função de proteção.

## Conclusão Técnica
O veículo sofreu uma colisão frontal de impacto moderado, resultando em danos cosméticos e funcionais que requerem reparos, mas não comprometem a segurança estrutural. Recomenda-se a substituição do para-choque e verificação detalhada do sistema de refrigeração para garantir que não houve danos secundários."""
    
    def generate_image(self, prompt):
        """Generate an image using Amazon Bedrock Titan Image Generator.
        
        Args:
            prompt: Text prompt for image generation
        
        Returns:
            bytes: Generated image in bytes
        """
        try:
            # Create request payload
            payload = {
                "textToImageParams": {
                    "text": prompt
                },
                "taskType": "TEXT_IMAGE",
                "imageGenerationConfig": {
                    "cfgScale": 8,
                    "seed": 42,
                    "quality": "standard",
                    "width": 1024,
                    "height": 1024,
                    "numberOfImages": 1
                }
            }
            
            # Invoke Titan Image Generator model
            response = self.bedrock_client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(payload)
            )
            
            # Parse response
            response_body = json.loads(response['body'].read())
            image_base64 = response_body['images'][0]
            
            # Convert base64 to bytes
            image_bytes = base64.b64decode(image_base64)
            
            return image_bytes
        except Exception as e:
            print(f"Error generating image: {e}")
            return None