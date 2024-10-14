# backend/Dockerfile
FROM python:3.12-slim

# Instala as dependências do sistema
RUN apt-get update && apt-get install -y \
    cmake \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de requisitos
COPY requirements.txt .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação
COPY . .

# Expõe a porta que o FastAPI usará
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]