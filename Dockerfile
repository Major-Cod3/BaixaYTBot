# Use uma imagem base do Python
FROM python:3.9-slim

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie o arquivo requirements.txt e instale as dependências
COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN . venv/bin/activate && pip install --upgrade pip && pip install pytube && pip install -r requirements.txt

# Copie todo o código do projeto para o contêiner
COPY . .

# Defina as variáveis de ambiente, se necessário
ENV TELEGRAM_TOKEN=${TELEGRAM_TOKEN}

# Exponha a porta necessária para o seu aplicativo
EXPOSE 8080  # Substitua 8080 pela porta que o seu aplicativo utiliza

# Comando para iniciar o bot
CMD ["python", "Bot.py"]
