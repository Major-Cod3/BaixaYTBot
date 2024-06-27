"""
Bot para Telegram que baixa vídeos e áudios do YouTube.

Autor: Ricardo
Contato: ricardodejesusbarbosa4@gmail.com
GitHub: https://github.com/Ricardo184
Instagram: https://www.instagram.com/ricardo_tx_

Este código está licenciado sob a Licença MIT.
"""

from pytube import YouTube
import telebot
import re
from telebot import types
import os

TOKEN = 'seu_token_aqui'  # Token do bot do Telegram
URL = ''  # Variável global para armazenar a URL do vídeo
pix_key = "a333a8d1-4978-4bb0-950b-e553ca6e1761"  # Chave PIX para doações
bot = telebot.TeleBot(TOKEN, parse_mode='Markdown')  # Inicializa o bot com o token e define o modo de parseamento


@bot.message_handler(commands=['start'])
def handle_message(message):
    # Responde ao comando /start com uma mensagem de boas-vindas e instruções
    bot.reply_to(message, "Olá! Bem-vindo ao nosso bot para baixar vídeos do YouTube.\n\n"
        "Para usá-lo, compartilhe o link do vídeo que deseja baixar.\n\n"
        "Se você quiser fazer uma doação, use o comando /donate.\nPara saber mais sobre o autor, use /autor.")


@bot.message_handler(commands=['autor'])
def send_author_info(message):
    # Responde ao comando /autor com informações sobre o autor
    author_info = f"""
    Eu sou Ricardo, um adolescente apaixonada por tecnologia e programação. Faço bots para Telegram por diversão e para aprender mais sobre desenvolvimento. Se você quiser saber mais sobre meus projetos ou entrar em contato, aqui estão algumas formas:
    
    - *GitHub:* https://github.com/Ricardo184
    - *Email:* ricardo.major.j@gmail.com
    - *instagram:* https://www.instagram.com/ricardo_tx_
    - *Chave PIX para doações:* `{pix_key}`
    
    Obrigado por usar meu bot! :)
    """
    bot.reply_to(message, author_info)


@bot.message_handler(commands=['donate'])
def send_donation_info(message):
    # Responde ao comando /donate com informações sobre doações
    donation_message = (
        "Se você deseja fazer uma doação, por favor use a chave PIX abaixo:\n\n"
        f"*Chave PIX:* `{pix_key}`\n\n"
        "Toque e segure na chave para copiar. Muito obrigado pelo seu apoio!"
    )
    bot.reply_to(message, donation_message)


def audio(chat, url):
    # Função para baixar o áudio de um vídeo do YouTube e enviá-lo no chat
    yt = YouTube(url)
    bot.send_message(chat, "Baixando Áudio...")
    audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
    audio_stream.download(output_path='download')
    files = os.listdir('download')
    for file in files:
        if file.endswith('.mp3') or file.endswith('.webm'):
            file_path = os.path.join('download', file)
            with open(file_path, 'rb') as audio_file:
                bot.send_audio(chat, audio_file)
            os.remove(f'download/{file}')


def video(chat, url):
    # Função para baixar o vídeo do YouTube e enviá-lo no chat
    yt = YouTube(url)
    bot.send_message(chat, "Baixando Vídeo...")
    yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(output_path='download')
    files = os.listdir('download')
    for file in files:
        if file.endswith('.mp4'):
            with open(f"download/{file}", 'rb') as video_file:
                bot.send_video(chat, video_file)
            os.remove(f'download/{file}')


def inline_options():
    # Função que cria botões inline para o usuário escolher entre baixar vídeo ou áudio
    markup = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton('vídeo', callback_data='vídeo')
    item2 = types.InlineKeyboardButton('áudio', callback_data='áudio')
    markup.add(item1, item2)
    return markup


@bot.message_handler(func=lambda message: True)
def dowlond(mensagen):
    # Função que lida com as mensagens do usuário
    global URL
    padrao_youtube = r'(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([A-Za-z0-9_-]{11})'
    url_yt = re.match(padrao_youtube, f'{mensagen.text}')
    padrao_url = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
    
    if url_yt:
        URL = url_yt.group(0)
        bot.send_message(mensagen.chat.id, "Baixa Vídeo Como", reply_markup=inline_options())
    elif re.match(padrao_url, f'{mensagen.text}'):
        bot.reply_to(mensagen, 'Desculpe, só é possível baixar vídeos do YouTube com este bot.')


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    # Função que lida com os botões inline
    global URL
    if call.data == 'vídeo':
        video(call.message.chat.id, URL)
    elif call.data == 'áudio':
        audio(call.message.chat.id, URL)
    bot.answer_callback_query(call.id)


bot.polling(none_stop=True)  # Inicia o polling do bot, mantendo-o ativo
