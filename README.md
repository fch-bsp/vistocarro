# VistoCarro - Sistema Profissional de Vistoria Veicular

![VistoCarro](https://img.shields.io/badge/VistoCarro-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0.0-red)

## Visão Geral


![Image](https://github.com/user-attachments/assets/d1174ff0-9565-4cf7-9ca2-5e1e17ab8dd9)
![Image](https://github.com/user-attachments/assets/94076283-f6ef-4264-b0c5-551e7ef398c1)
![Image](https://github.com/user-attachments/assets/104151a5-b5ee-4e57-85ea-86e4f6fca301)


VistoCarro é uma solução avançada para vistoria veicular que utiliza Inteligência Artificial para análise automatizada de danos em veículos. Desenvolvido com tecnologias de ponta como Google Gemini Vision e integração com AWS, o sistema oferece uma plataforma completa para profissionais do setor automotivo realizarem vistorias precisas e gerarem relatórios detalhados.

## Principais Funcionalidades

### 📸 Análise Inteligente de Imagens
- Processamento de múltiplas imagens de veículos simultaneamente
- Detecção automática de avarias, danos e problemas estruturais
- Identificação precisa de componentes danificados

### 📊 Relatórios Profissionais
- Geração automática de relatórios detalhados em formato PDF
- Documentação técnica com descrição das avarias encontradas
- Exportação de dados em formato TXT para integração com outros sistemas

### 💬 Assistente Virtual Especializado
- Assistente "Gemini" integrado para responder dúvidas técnicas
- Consulta contextual baseada nas imagens analisadas
- Suporte à tomada de decisão durante o processo de vistoria

### ☁️ Armazenamento Seguro na Nuvem
- Integração com Amazon S3 para armazenamento seguro de imagens e relatórios
- Acesso persistente aos dados de vistorias anteriores
- Backup automático de todas as informações processadas

### 🔄 Sistema RAG (Retrieval-Augmented Generation)
- Utilização de tecnologia RAG para respostas mais precisas e contextualizadas
- Consulta a base de conhecimento especializada em vistorias veiculares

## Arquitetura do Sistema

O VistoCarro foi desenvolvido com uma arquitetura modular que permite fácil manutenção e escalabilidade:

```
vistocarro/
├── app.py                    # Aplicação principal Streamlit
├── utils/                    # Módulos de funcionalidades
│   ├── gemini_handler.py     # Integração com Google Gemini Vision
│   ├── bedrock_handler.py    # Integração com AWS Bedrock
│   ├── s3_handler.py         # Gerenciamento de armazenamento no S3
│   ├── report_generator.py   # Geração de relatórios profissionais
│   ├── image_analyzer.py     # Análise avançada de imagens
│   └── rag_system.py         # Sistema RAG para consultas contextuais
├── storage/                  # Armazenamento local temporário
│   ├── uploads/              # Imagens enviadas para análise
│   └── reports/              # Relatórios gerados
└── Dockerfile                # Configuração para containerização
```

## Requisitos Técnicos

- Python 3.8+
- Conta AWS com acesso ao Amazon S3
- Chave de API do Google Gemini
- Credenciais configuradas nos arquivos `.env` e `.env_gemini`

## Instalação e Configuração

### 1. Clone o repositório
```bash
git clone <repository-url>
cd vistocarro
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure as credenciais AWS
Crie um arquivo `.env` com as seguintes informações:
```
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=your_region
S3_BUCKET=your_bucket_name
```

### 4. Configure a API do Google Gemini
Crie um arquivo `.env_gemini` com sua chave de API:
```
GOOGLE_API_KEY=your_gemini_api_key
```

## Execução da Aplicação

### Método Padrão
```bash
streamlit run app.py
```

### Usando Script de Inicialização
```bash
./run.sh
```

### Usando Docker
```bash
docker build -t vistocarro .
docker run -p 8501:8501 vistocarro
```

## Fluxo de Trabalho

1. **Upload de Imagens**: Faça upload de uma ou mais imagens do veículo a ser vistoriado
2. **Análise Automatizada**: O sistema processa as imagens utilizando IA para identificar avarias
3. **Revisão dos Resultados**: Visualize a análise detalhada de cada problema identificado
4. **Consulta ao Assistente**: Utilize o assistente virtual para esclarecer dúvidas técnicas
5. **Geração de Relatórios**: Exporte relatórios profissionais em PDF para documentação
6. **Armazenamento**: Todos os dados são automaticamente salvos na nuvem para consultas futuras

## Segurança e Conformidade

- Todas as imagens e dados são processados com segurança
- Armazenamento criptografado no Amazon S3
- Conformidade com padrões de proteção de dados

---

© 2024 VistoCarro | Sistema Profissional de Vistoria Veicular
