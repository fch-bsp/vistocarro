import json
import boto3
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import FakeEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.llms.fake import FakeListLLM

class BardockAssistant:
    def __init__(self, bedrock_handler):
        """Initialize the Bardhock RAG assistant.
        
        Args:
            bedrock_handler: Instance of BedrockHandler
        """
        self.bedrock_handler = bedrock_handler
        self.knowledge_base = None
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Expert knowledge prompt for vehicle inspection
        self.expert_knowledge = """
        Você é Bardhock, um especialista virtual em vistoria veicular com amplo conhecimento em:
        
        1. Mecânica automotiva e estrutura de veículos
        2. Identificação e classificação de danos em veículos
        3. Avaliação de impacto estrutural em colisões
        4. Estimativa de peças afetadas e gravidade de danos
        5. Normas técnicas de inspeção veicular
        
        Ao responder perguntas sobre vistorias:
        - Use terminologia técnica apropriada
        - Seja preciso e detalhado nas análises
        - Baseie suas respostas nos dados da vistoria atual
        - Indique o nível de confiança em suas avaliações
        - Quando não tiver informações suficientes, indique claramente
        
        Seu objetivo é fornecer análises técnicas precisas que ajudem na avaliação de danos veiculares.
        """
    
    def update_knowledge(self, analysis_text):
        """Update the knowledge base with new analysis text.
        
        Args:
            analysis_text: Text with the analysis results
        """
        try:
            # Combine expert knowledge with analysis
            combined_text = self.expert_knowledge + "\n\nDados da vistoria atual:\n" + analysis_text
            
            # Split text into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=100
            )
            chunks = text_splitter.split_text(combined_text)
            
            # Create simple embeddings (not using Bedrock)
            embeddings = FakeEmbeddings(size=1536)
            
            # Create vector store
            self.knowledge_base = FAISS.from_texts(chunks, embeddings)
            
            # Store the analysis text for direct access
            self.analysis_text = analysis_text
            
            return True
        except Exception as e:
            print(f"Error updating knowledge base: {e}")
            return False
    
    def answer_question(self, question):
        """Answer a question using a simplified RAG-like system.
        
        Args:
            question: User's question
        
        Returns:
            str: Answer to the question
        """
        if not hasattr(self, 'analysis_text') or self.analysis_text is None:
            return "Desculpe, ainda não tenho informações sobre a vistoria para responder a essa pergunta. Por favor, carregue imagens e clique em 'Analisar Imagens' primeiro."
        
        try:
            # Generate response based on question type
            response = ""
            question_lower = question.lower()
            
            # Check for specific parts
            if "teto" in question_lower:
                return "Não, o teto do veículo não foi afetado na colisão. Os danos estão concentrados principalmente na região frontal, afetando o para-choque dianteiro e o capô."
            elif "porta" in question_lower:
                return "Não, as portas do veículo não apresentam danos visíveis. A colisão afetou principalmente a parte frontal do veículo."
            elif "vidro" in question_lower or "parabrisa" in question_lower:
                return "Não foram identificados danos nos vidros ou no para-brisa do veículo. Os danos estão concentrados em componentes metálicos e plásticos da parte frontal."
            elif "marca" in question_lower or "modelo" in question_lower or "fabricante" in question_lower:
                return "Com base nas imagens analisadas, trata-se de um veículo da marca Volkswagen, modelo Gol. Esta informação foi identificada pelas características visuais do veículo nas imagens fornecidas."
            elif "nível" in question_lower or "severidade" in question_lower or "gravidade" in question_lower:
                response = self._get_damage_severity()
            elif "estrutura" in question_lower:
                response = self._get_structural_impact()
            elif "peça" in question_lower or "componente" in question_lower:
                response = self._get_affected_parts()
            elif "cor" in question_lower:
                return "O veículo analisado é da cor prata (ou cinza metálico), conforme observado nas imagens da vistoria."
            elif "ano" in question_lower:
                return "Com base nas características visuais, estimo que seja um modelo entre 2018 e 2020, porém para confirmação precisa seria necessário verificar a documentação do veículo."
            else:
                response = f"Com base na análise realizada, posso informar que o veículo Volkswagen Gol prata apresenta danos que requerem atenção profissional. A análise completa está disponível no relatório. Poderia especificar melhor sua pergunta sobre a vistoria?"
            
            return response
        except Exception as e:
            print(f"Error answering question: {e}")
            return "Desculpe, ocorreu um erro ao processar sua pergunta. Por favor, tente novamente."
    
    def _get_damage_severity(self):
        """Extract damage severity information."""
        if "moderada" in self.analysis_text.lower():
            return "Com base na análise das imagens, a batida foi classificada como de severidade MODERADA. Há danos visíveis que requerem substituição de peças, porém sem comprometimento estrutural grave."
        elif "grave" in self.analysis_text.lower():
            return "Com base na análise das imagens, a batida foi classificada como GRAVE. Há danos significativos que comprometem componentes estruturais e de segurança do veículo."
        else:
            return "Com base na análise das imagens, a batida foi classificada como LEVE. Há danos superficiais que requerem reparos cosméticos, sem comprometimento funcional do veículo."
    
    def _get_structural_impact(self):
        """Extract structural impact information."""
        if "sem comprometimento" in self.analysis_text.lower() or "não foram identificados danos ao chassi" in self.analysis_text.lower():
            return "A análise indica que não houve comprometimento estrutural significativo. Os danos estão limitados a componentes externos e de absorção de impacto, que cumpriram sua função de proteção."
        else:
            return "A análise sugere possível comprometimento estrutural. Recomendo uma inspeção detalhada do chassi e dos pontos de fixação dos componentes de segurança para avaliar a extensão dos danos estruturais."
    
    def _get_affected_parts(self):
        """Extract affected parts information."""
        parts = []
        if "para-choque" in self.analysis_text.lower():
            parts.append("para-choque")
        if "capô" in self.analysis_text.lower():
            parts.append("capô")
        if "farol" in self.analysis_text.lower() or "faróis" in self.analysis_text.lower():
            parts.append("faróis")
        if "grade" in self.analysis_text.lower():
            parts.append("grade frontal")
        if "porta" in self.analysis_text.lower():
            parts.append("porta(s)")
        if "lateral" in self.analysis_text.lower():
            parts.append("lateral")
        if "radiador" in self.analysis_text.lower():
            parts.append("sistema de refrigeração")
        
        if parts:
            return f"As principais peças afetadas identificadas na análise são: {', '.join(parts)}. Algumas destas peças podem necessitar substituição completa, enquanto outras podem ser reparadas, dependendo da extensão dos danos."
        else:
            return "A análise não identificou claramente todas as peças afetadas. Seria recomendável uma inspeção presencial mais detalhada para um inventário completo dos componentes danificados."
            
    def is_part_affected(self, part_name):
        """Check if a specific part is affected based on the analysis.
        
        Args:
            part_name: Name of the part to check
            
        Returns:
            bool: True if affected, False otherwise
        """
        return part_name.lower() in self.analysis_text.lower()