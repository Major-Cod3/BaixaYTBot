from pytube import YouTube
import telebot
import re
from telebot import types
import os

TOKEN = 'seu_token_aqui'
URL = ''
pix_key = "a333a8d1-4978-4bb0-950b-e553ca6e1761"
bot = telebot.TeleBot(TOKEN, parse_mode='Markdown')

# Manipulador de mensagem para o comando /start
@bot.message_handler(commands=['start'])
def handle_message(message):
    # Responde ao usuário com uma mensagem de boas-vindas e instruções
    bot.reply_to(message, "Olá! Bem-vindo ao nosso bot para baixar vídeos do YouTube.\n\n"
        "Para usá-lo, compartilhe o link do vídeo que deseja baixar.\n\n"
        "Se você quiser fazer uma doação, use o comando /donate.\nPara saber mais sobre o autor, use /autor.")

# Manipulador de mensagem para o comando /autor
@bot.message_handler(commands=['autor'])
def send_author_info(message):
    # Mensagem com informações sobre o autor
    author_info = f"""
    Eu sou Ricardo, um adolescente apaixonada por tecnologia e programação. Faço bots para Telegram por diversão e para aprender mais sobre desenvolvimento. Se você quiser saber mais sobre meus projetos ou entrar em contato, aqui estão algumas formas:
    
    - *GitHub:* https://github.com/Ricardo184
    - *Email:* ricardodejesusbarbosa4@gmail.com
    - *Instagram:* https://www.instagram.com/ricardo_tx_
    - *Chave PIX para doações:* `{pix_key}`
    
    Obrigado por usar meu bot! :)
    """
    # Envia a mensagem com informações do autor
    bot.reply_to(message, author_info)

# Manipulador de mensagem para o comando /donate
@bot.message_handler(commands=['donate'])
def send_donation_info(message):
    # Mensagem com informações para doação
    donation_message = (
        "Se você deseja fazer uma doação, por favor use a chave PIX abaixo:\n\n"
        f"*Chave PIX:* `{pix_key}`\n\n"
        "Toque e segure na chave para copiar. Muito obrigado pelo seu apoio!"
    )
    # Envia a mensagem com informações para doação
    bot.reply_to(message, donation_message)

# Função para baixar e enviar áudio do YouTube
def download_audio(chat, url):
    yt = YouTube(url)
    bot.send_message(chat, "Baixando Áudio...")
    audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
    audio_stream.download(output_path='download')
    files = os.listdir('download')
    for file in files:
        if file.endswith('.mp3') or file.endswith('.webm'):
            file_path = os.path.join('download', file)
            audio = open(file_path, 'rb')
            return audio

# Função para baixar e enviar vídeo do YouTube
def download_video(chat, url):
    yt = YouTube(url)
    bot.send_message(chat, "Baixando Vídeo...")
    yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(output_path='download')
    file_path = os.path.join('download', f"{yt.title}.mp4")
    video = open(file_path, 'rb')
    return video

# Função para criar e retornar opções de botões inline
def inline_options():
    markup = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton('vídeo', callback_data='vídeo')
    item2 = types.InlineKeyboardButton('áudio', callback_data='áudio')
    markup.add(item1, item2)
    return markup

# Manipulador de mensagem para qualquer mensagem que não seja um comando
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global URL
    youtube_pattern = r'(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([A-Za-z0-9_-]{11})'
    url_match = re.match(youtube_pattern, f'{message.text}')
    if url_match:
        URL = url_match.group(0)
        bot.send_message(message.chat.id, "Baixar como:", reply_markup=inline_options())

# Manipulador de callback para os botões inline
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    global URL
    if call.data == 'vídeo':
        bot.send_video(call.message.chat.id, download_video(call.message.chat.id, URL))
    elif call.data == 'áudio':
        bot.send_audio(call.message.chat.id, download_audio(call.message.chat.id, URL))
    bot.answer_callback_query(call.id)

# Limpeza dos arquivos na pasta 'download' ao iniciar o bot
files = os.listdir('download')
for file in files:
    if file.endswith('.mp4') or file.endswith('.mp3') or file.endswith('.webm'):
        os.remove(os.path.join('download', file))

# Inicia o bot para receber e processar mensagens
bot.polling(none_stop=True)
