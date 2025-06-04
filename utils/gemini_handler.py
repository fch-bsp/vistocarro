import os
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import io

class GeminiHandler:
    """Handler for Google Gemini API."""
    
    def __init__(self):
        """Initialize the Gemini API client."""
        # Load environment variables from .env_gemini
        dotenv_path = "/home/fernandohoras/Documentos/Projeto_Validado/Vistoria_Veicular/.env_gemini"
        load_dotenv(dotenv_path)
        
        # Get API key directly from file if loading fails
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            try:
                with open(dotenv_path, 'r') as f:
                    for line in f:
                        if line.startswith('GOOGLE_API_KEY='):
                            api_key = line.strip().split('=', 1)[1]
                            break
            except Exception as e:
                print(f"Error reading .env_gemini file: {e}")
        
        # Use the new API key
        api_key = "AIzaSyDQJadHRonvqZmlCKJIN77lNWQtU7tGoPs"
        
        # Configure the Gemini API
        genai.configure(api_key=api_key)
        
        # Select the Gemini 1.5 Flash model for both image analysis and text generation
        # This model replaces the deprecated gemini-pro-vision
        self.vision_model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Use the same model for text generation
        self.text_model = genai.GenerativeModel('gemini-1.5-flash')
    
    def analyze_image(self, image_bytes):
        """Analyze an image using Gemini Vision.
        
        Args:
            image_bytes: The image content in bytes
            
        Returns:
            str: Analysis result
        """
        try:
            # Convert bytes to PIL Image
            img = Image.open(io.BytesIO(image_bytes))
            
            # Create prompt for vehicle damage analysis
            prompt = """Você é um especialista em vistoria veicular. Analise esta imagem de um veículo e forneça:
            
            1. Identificação do veículo (tipo, marca, modelo, cor)
            2. Localização dos danos (para-choque, porta, capô, etc.)
            3. Tipo de dano (amassado, arranhão, quebrado, etc.)
            4. Severidade do dano (leve, moderado, grave)
            5. Possível impacto na estrutura do veículo
            6. Estimativa de peças afetadas
            
            Forneça uma análise técnica e detalhada como um especialista em vistoria veicular.
            Seja preciso na identificação do veículo e dos danos com base no que você realmente vê na imagem.
            """
            
            # Generate content with the image using the updated model
            response = self.vision_model.generate_content([prompt, img])
            
            # Check if response has text attribute (newer versions)
            if hasattr(response, 'text'):
                return response.text
            # For older versions that might use different response structure
            elif hasattr(response, 'candidates'):
                return response.candidates[0].content.parts[0].text
            else:
                # Try to extract text from response in a different way
                return str(response)
                
        except Exception as e:
            print(f"Error analyzing image with Gemini: {e}")
            raise e
    
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

Seu relatório deve ser detalhado, técnico e organizado em seções claras com o título "RELATÓRIO DE VISTORIA VEICULAR".
Use apenas as informações das análises fornecidas, sem adicionar detalhes fictícios.
"""
            
            # Generate content with the updated model
            response = self.text_model.generate_content(prompt)
            
            # Check if response has text attribute (newer versions)
            if hasattr(response, 'text'):
                return response.text
            # For older versions that might use different response structure
            elif hasattr(response, 'candidates'):
                return response.candidates[0].content.parts[0].text
            else:
                # Try to extract text from response in a different way
                return str(response)
                
        except Exception as e:
            print(f"Error generating combined analysis with Gemini: {e}")
            raise e
    
    def answer_question(self, question, analysis_text):
        """Answer a question based on the analysis.
        
        Args:
            question: User's question
            analysis_text: The analysis text to base answers on
            
        Returns:
            str: Answer to the question
        """
        try:
            # Print debug info
            print(f"Analysis text is None: {analysis_text is None}")
            print(f"Analysis text type: {type(analysis_text)}")
            if analysis_text:
                print(f"Analysis text length: {len(analysis_text)}")
            
            # Use default analysis if None is provided
            if analysis_text is None or not analysis_text:
                from utils.default_analysis import DEFAULT_ANALYSIS
                analysis_text = DEFAULT_ANALYSIS
                print("Using DEFAULT_ANALYSIS as fallback")
                
            prompt = f"""Você é um especialista em vistoria veicular chamado Gemini. 
            Com base na seguinte análise de um veículo com avarias:

{analysis_text}

Responda à seguinte pergunta do usuário de forma técnica e precisa:

{question}

Importante: Responda apenas com base nas informações contidas na análise acima. 
Se a informação não estiver presente na análise, diga que não possui essa informação específica.
Não invente detalhes que não estejam na análise.
"""
            
            # Generate content with the updated model
            response = self.text_model.generate_content(prompt)
            
            # Check if response has text attribute (newer versions)
            if hasattr(response, 'text'):
                return response.text
            # For older versions that might use different response structure
            elif hasattr(response, 'candidates'):
                return response.candidates[0].content.parts[0].text
            else:
                # Try to extract text from response in a different way
                return str(response)
                
        except Exception as e:
            print(f"Error answering question with Gemini: {e}")
            return f"Desculpe, ocorreu um erro ao processar sua pergunta: {str(e)}. Por favor, tente novamente mais tarde."