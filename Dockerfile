# Use a imagem oficial do Python como imagem base
FROM python:3.8

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie os arquivos do bot para o diretório de trabalho
COPY . /app

# Instale as dependências do bot
RUN pip install -r requirements.txt

# Defina variáveis de ambiente (não inclua o token aqui para segurança)
ENV TELEGRAM_TOKEN=${TELEGRAM_TOKEN}

# Defina o ponto de entrada para o contêiner
CMD ["python", "Bot.py"]
