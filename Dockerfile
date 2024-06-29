# Instalação do python e criação de um usuário não-root
FROM python:3.9-slim

# Criação de um diretório de trabalho
WORKDIR /app

# Copia o arquivo requirements.txt e instala as dependências
COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN . venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

# Copia o código do projeto para o contêiner
COPY . .

# Define as variáveis de ambiente
ENV TELEGRAM_TOKEN=${TELEGRAM_TOKEN}

# Comando para iniciar o bot
CMD ["python", "Bot.py"]
