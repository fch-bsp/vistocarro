FROM python:3.10-slim

WORKDIR /app

# Instale as dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    procps \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Copie os arquivos do projeto
COPY . .

# Instale as dependências Python
RUN pip3 install -r requirements.txt

# Configure o Streamlit para aceitar conexões externas
RUN mkdir -p /root/.streamlit && \
    echo '\
[server]\n\
headless = true\n\
enableCORS = true\n\
enableXsrfProtection = false\n\
port = 8502\n\
address = "0.0.0.0"\n\
maxUploadSize = 200\n\
baseUrlPath = ""\n\
' > /root/.streamlit/config.toml

# Configure o Nginx para proxy reverso
RUN echo '\
server {\n\
    listen 8501;\n\
    server_name localhost;\n\
\n\
    location /_stcore/health {\n\
        return 200 "OK";\n\
        add_header Content-Type text/plain;\n\
    }\n\
\n\
    location / {\n\
        proxy_pass http://localhost:8502;\n\
        proxy_http_version 1.1;\n\
        proxy_set_header Upgrade $http_upgrade;\n\
        proxy_set_header Connection "upgrade";\n\
        proxy_set_header Host $host;\n\
        proxy_cache_bypass $http_upgrade;\n\
    }\n\
}\n\
' > /etc/nginx/conf.d/default.conf

# Crie um script de inicialização
RUN echo '#!/bin/bash\n\
# Inicie o Nginx\n\
nginx\n\
\n\
# Inicie o Streamlit\n\
exec streamlit run app.py --server.port=8502 --server.address=0.0.0.0\n\
' > /app/start.sh && chmod +x /app/start.sh

# Exponha a porta
EXPOSE 8501

# Configure variáveis de ambiente
ENV PYTHONUNBUFFERED=1

# Execute o script de inicialização
CMD ["/app/start.sh"]