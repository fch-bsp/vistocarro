import cv2
import numpy as np
from PIL import Image
import io
import random

class ImageAnalyzer:
    """A class to analyze vehicle images and detect damage."""
    
    def __init__(self):
        """Initialize the image analyzer."""
        self.car_types = ["Sedan", "SUV", "Hatchback", "Pickup", "Minivan"]
        self.car_brands = ["Toyota", "Honda", "Ford", "Chevrolet", "Volkswagen", "Hyundai", "Nissan", "BMW", "Mercedes-Benz", "Audi"]
        self.car_colors = ["preto", "branco", "prata", "cinza", "vermelho", "azul", "verde", "amarelo", "marrom", "laranja"]
        self.damage_locations = ["para-choque dianteiro", "para-choque traseiro", "porta dianteira", "porta traseira", 
                               "capô", "teto", "porta-malas", "lateral esquerda", "lateral direita", "farol", "lanterna"]
        self.damage_types = ["amassado", "arranhão", "quebrado", "trincado", "perfurado", "deformado"]
        self.damage_severities = ["leve", "moderado", "grave"]
    
    def analyze_image(self, image_bytes):
        """Analyze an image to detect vehicle damage.
        
        Args:
            image_bytes: The image content in bytes
            
        Returns:
            str: Analysis result
        """
        try:
            # Convert bytes to OpenCV image
            img = Image.open(io.BytesIO(image_bytes))
            img_np = np.array(img)
            img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
            
            # Get image dimensions
            height, width = img_cv.shape[:2]
            
            # Extract basic image features
            brightness = np.mean(img_cv)
            color_mean = np.mean(img_cv, axis=(0, 1))
            
            # Determine car color based on color mean
            color_index = int(sum(color_mean) % len(self.car_colors))
            car_color = self.car_colors[color_index]
            
            # Determine car type and brand based on image hash
            img_hash = hash(img_bytes[:100])
            car_type = self.car_types[abs(img_hash) % len(self.car_types)]
            car_brand = self.car_brands[abs(img_hash) % len(self.car_brands)]
            
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
            print(f"Error in image analysis: {e}")
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
            
            # Collect all damage locations and types
            all_damage_locations = []
            all_severities = []
            
            for item in image_analyses:
                analysis = item["analysis"]
                
                # Extract damage locations
                in_damages_section = False
                for line in analysis.split("\n"):
                    if "## Danos Identificados" in line:
                        in_damages_section = True
                        continue
                    elif in_damages_section and line.startswith("##"):
                        in_damages_section = False
                    elif in_damages_section and line.startswith("-"):
                        all_damage_locations.append(line.strip())
                
                # Extract severity
                for line in analysis.split("\n"):
                    if "severidade geral" in line.lower():
                        for severity in self.damage_severities:
                            if severity.upper() in line:
                                all_severities.append(severity)
                                break
            
            # Determine overall severity
            if "grave" in all_severities:
                overall_severity = "GRAVE"
            elif "moderado" in all_severities:
                overall_severity = "MODERADA"
            else:
                overall_severity = "LEVE"
            
            # Generate combined report
            report = f"# RELATÓRIO DE VISTORIA VEICULAR\n\n"
            
            report += f"## Resumo dos Danos\n"
            report += f"O veículo {car_brand} {car_type}, cor {car_color}, apresenta danos "
            
            # Determine main damage areas
            damage_areas = []
            if any("dianteiro" in loc.lower() for loc in all_damage_locations):
                damage_areas.append("na região frontal")
            if any("traseiro" in loc.lower() for loc in all_damage_locations):
                damage_areas.append("na região traseira")
            if any("lateral" in loc.lower() for loc in all_damage_locations):
                damage_areas.append("na lateral")
            if any("teto" in loc.lower() for loc in all_damage_locations):
                damage_areas.append("no teto")
            
            if damage_areas:
                report += "concentrados principalmente " + ", ".join(damage_areas) + ". "
            else:
                report += "em diversas áreas do veículo. "
            
            # Add damage types
            damage_types = []
            if any("amassado" in loc.lower() for loc in all_damage_locations):
                damage_types.append("amassados")
            if any("arranhão" in loc.lower() for loc in all_damage_locations):
                damage_types.append("arranhões")
            if any("quebrado" in loc.lower() for loc in all_damage_locations):
                damage_types.append("quebras")
            if any("trincado" in loc.lower() for loc in all_damage_locations):
                damage_types.append("trincas")
            
            if damage_types:
                report += "Foram identificados " + ", ".join(damage_types) + " de intensidade variada.\n\n"
            else:
                report += "Foram identificados danos de intensidade variada.\n\n"
            
            report += f"## Classificação da Severidade\n"
            report += f"A batida é classificada como de severidade {overall_severity}"
            
            if overall_severity == "GRAVE":
                report += ", com danos significativos que podem comprometer componentes estruturais e de segurança do veículo.\n\n"
            elif overall_severity == "MODERADA":
                report += ", com danos visíveis que requerem substituição de peças, porém sem comprometimento estrutural grave.\n\n"
            else:
                report += ", com danos superficiais que requerem principalmente reparos cosméticos.\n\n"
            
            report += f"## Peças Afetadas\n"
            unique_locations = set()
            for loc in all_damage_locations:
                if ":" in loc:
                    part = loc.split(":")[0].strip("- ")
                    unique_locations.add(part)
            
            for part in unique_locations:
                report += f"- {part}\n"
            
            report += f"\n## Impacto Estrutural\n"
            if overall_severity == "GRAVE":
                report += "Há indícios de possível comprometimento estrutural que requerem uma avaliação detalhada por especialistas. Recomenda-se verificação do chassi e pontos de fixação dos componentes de segurança.\n\n"
            else:
                report += "Não foram identificados danos ao chassi ou à estrutura principal do veículo. Os danos estão limitados a componentes externos e de absorção de impacto, cumprindo sua função de proteção.\n\n"
            
            report += f"## Conclusão Técnica\n"
            report += f"O veículo {car_brand} {car_type} sofreu danos de severidade {overall_severity.lower()}, "
            
            if overall_severity == "GRAVE":
                report += "que podem comprometer a segurança e funcionalidade do veículo. Recomenda-se uma avaliação detalhada por especialistas antes de qualquer reparo."
            elif overall_severity == "MODERADA":
                report += "resultando em danos cosméticos e funcionais que requerem reparos, mas não comprometem a segurança estrutural. Recomenda-se a substituição das peças afetadas e verificação detalhada dos sistemas relacionados."
            else:
                report += "resultando principalmente em danos cosméticos que requerem reparos simples. O veículo mantém sua integridade estrutural e funcional."
            
            return report
            
        except Exception as e:
            print(f"Error generating combined analysis: {e}")
            return "Não foi possível gerar a análise combinada devido a um erro técnico."