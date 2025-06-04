# Sistema de Vistoria Veicular com Google Gemini

Um aplicativo completo em Python com interface Streamlit para análise de imagens de veículos com avarias usando IA generativa do Google Gemini.

## Funcionalidades

- Upload de uma ou múltiplas imagens de veículos com avarias
- Análise automática das imagens usando Google Gemini Vision
- Geração de relatórios detalhados em PDF e TXT
- Assistente virtual "Gemini" para responder perguntas sobre a vistoria
- Armazenamento de imagens e relatórios no Amazon S3

## Requisitos

- Python 3.8+
- Conta AWS com acesso ao Amazon S3
- Chave de API do Google Gemini
- Credenciais configuradas nos arquivos `.env` e `.env_gemini`

## Instalação

1. Clone o repositório:
```
git clone <repository-url>
cd Vistoria_Veicular
```

2. Instale as dependências:
```
pip install -r requirements.txt
```

3. Configure as credenciais AWS no arquivo `.env`:
```
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=your_region
S3_BUCKET=your_bucket_name
```

4. Configure a chave de API do Google Gemini no arquivo `.env_gemini`:
```
GOOGLE_API_KEY=your_gemini_api_key
```

## Execução

Execute o aplicativo Streamlit:
```
streamlit run app.py
```

Ou use o script:
```
./run.sh
```

## Estrutura do Projeto

- `app.py`: Aplicativo principal Streamlit
- `utils/`: Módulos utilitários
  - `gemini_handler.py`: Integração com Google Gemini para análise de imagens
  - `s3_handler.py`: Gerenciamento de armazenamento no S3
  - `report_generator.py`: Geração de relatórios PDF e TXT

## Fluxo de Uso

1. Faça upload de uma ou mais imagens do veículo com avarias
2. Clique em "Analisar Imagens" para iniciar a análise com IA
3. Visualize o resultado da análise e os relatórios gerados
4. Interaja com o assistente Gemini para fazer perguntas sobre a vistoria
5. Baixe os relatórios PDF e TXT gerados