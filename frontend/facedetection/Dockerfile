# frontend/Dockerfile
FROM node:18-alpine

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de pacotes
COPY package.json package-lock.json ./

# Instala as dependências
RUN npm install

# Copia o restante do código da aplicação
COPY . .

# Compila a aplicação
RUN npm run build

# Expõe a porta que o Next.js usará
EXPOSE 3000

# Comando para rodar a aplicação
CMD ["npm", "start"]