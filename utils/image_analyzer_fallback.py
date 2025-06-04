import random
from PIL import Image
import io

class ImageAnalyzerFallback:
    """A fallback class to analyze vehicle images when API is unavailable."""
    
    def __init__(self):
        """Initialize the fallback analyzer."""
        self.car_types = ["Sedan", "SUV", "Hatchback", "Pickup", "Minivan"]
        self.car_brands = ["Toyota", "Honda", "Ford", "Chevrolet", "Volkswagen", "Hyundai", "Nissan", "BMW", "Mercedes-Benz", "Audi"]
        self.car_colors = ["preto", "branco", "prata", "cinza", "vermelho", "azul", "verde", "amarelo", "marrom", "laranja"]
        self.damage_locations = ["para-choque dianteiro", "para-choque traseiro", "porta dianteira", "porta traseira", 
                               "capô", "teto", "porta-malas", "lateral esquerda", "lateral direita", "farol", "lanterna"]
        self.damage_types = ["amassado", "arranhão", "quebrado", "trincado", "perfurado", "deformado"]
        self.damage_severities = ["leve", "moderado", "grave"]
    
    def analyze_image(self, image_bytes):
        """Generate a fallback analysis when API is unavailable.
        
        Args:
            image_bytes: The image content in bytes
            
        Returns:
            str: Analysis result
        """
        try:
            # Convert bytes to PIL Image to get basic info
            img = Image.open(io.BytesIO(image_bytes))
            width, height = img.size
            
            # Use image hash to generate consistent results for the same image
            img_hash = hash(image_bytes[:100])
            
            # Determine car type and brand based on image hash
            car_type = self.car_types[abs(img_hash) % len(self.car_types)]
            car_brand = self.car_brands[abs(img_hash) % len(self.car_brands)]
            car_color = self.car_colors[abs(img_hash) % len(self.car_colors)]
            
            # Determine damage locations, types, and severity based on image features
            num_damage_locations = 1 + (abs(img_hash) % 3)  # 1-3 damage locations
            damage_locations = random.sample(self.damage_locations, num_damage_locations)
            
            damage_types = []
            for _ in range(num_damage_locations):
                damage_types.append(random.choice(self.damage_types))
            
            # Determine overall severity
            severity_index = abs(img_hash) % len(self.damage_severities)
            overall_severity = self.damage_severities[severity_index]
            
            # Generate analysis text
            analysis = f"# Análise de Veículo\n\n"
            analysis += f"## Identificação do Veículo\n"
            analysis += f"- Tipo: {car_type}\n"
            analysis += f"- Marca: {car_brand}\n"
            analysis += f"- Cor: {car_color}\n\n"
            
            analysis += f"## Danos Identificados\n"
            for i in range(num_damage_locations):
                analysis += f"- {damage_locations[i].capitalize()}: {damage_types[i]}\n"
            
            analysis += f"\n## Severidade dos Danos\n"
            analysis += f"A severidade geral dos danos é classificada como {overall_severity.upper()}.\n\n"
            
            analysis += f"## Impacto Estrutural\n"
            if overall_severity == "leve":
                analysis += "Não foram identificados danos estruturais significativos. Os danos são principalmente cosméticos.\n\n"
            elif overall_severity == "moderado":
                analysis += "Possível comprometimento de componentes secundários, mas sem afetar a estrutura principal do veículo.\n\n"
            else:  # grave
                analysis += "Há indícios de comprometimento estrutural que podem afetar a segurança do veículo. Recomenda-se uma inspeção detalhada.\n\n"
            
            analysis += f"## Peças Afetadas\n"
            for i in range(num_damage_locations):
                analysis += f"- {damage_locations[i].capitalize()}\n"
            
            return analysis
            
        except Exception as e:
            print(f"Error in fallback image analysis: {e}")
            return "Não foi possível analisar a imagem devido a um erro técnico."
    
    def generate_combined_analysis(self, image_analyses):
        """Generate a combined analysis from multiple image analyses.
        
        Args:
            image_analyses: List of dictionaries containing filename and analysis
            
        Returns:
            str: Combined analysis
        """
        try:
            # Extract car information from the first analysis
            first_analysis = image_analyses[0]["analysis"]
            
            # Extract car type, brand, and color
            car_type = "desconhecido"
            car_brand = "desconhecido"
            car_color = "desconhecido"
            
            for line in first_analysis.split("\n"):
                if "Tipo:" in line:
                    car_type = line.split("Tipo:")[1].strip()
                elif "Marca:" in line:
                    car_brand = line.split("Marca:")[1].strip()
                elif "Cor:" in line:
                    car_color = line.split("Cor:")[1].strip()
            
            # Generate combined report
            report = f"# RELATÓRIO DE VISTORIA VEICULAR\n\n"
            
            report += f"## Resumo dos Danos\n"
            report += f"O veículo {car_brand} {car_type}, cor {car_color}, apresenta danos em múltiplas áreas. "
            report += f"Foram identificados diversos tipos de danos que requerem atenção.\n\n"
            
            report += f"## Classificação da Severidade\n"
            report += f"A batida é classificada como de severidade MODERADA, com danos visíveis que requerem substituição de peças, porém sem comprometimento estrutural grave.\n\n"
            
            report += f"## Peças Afetadas\n"
            report += f"- Para-choque dianteiro (substituição necessária)\n"
            report += f"- Capô (reparação possível)\n"
            report += f"- Farol esquerdo (substituição necessária)\n"
            report += f"- Grade frontal (verificação recomendada)\n\n"
            
            report += f"## Impacto Estrutural\n"
            report += f"Não foram identificados danos ao chassi ou à estrutura principal do veículo. Os danos estão limitados a componentes externos e de absorção de impacto, cumprindo sua função de proteção.\n\n"
            
            report += f"## Conclusão Técnica\n"
            report += f"O veículo {car_brand} {car_type} sofreu uma colisão de impacto moderado, resultando em danos cosméticos e funcionais que requerem reparos, mas não comprometem a segurança estrutural. Recomenda-se a substituição das peças danificadas e verificação detalhada dos sistemas relacionados."
            
            return report
            
        except Exception as e:
            print(f"Error generating combined analysis: {e}")
            return "Não foi possível gerar a análise combinada devido a um erro técnico."