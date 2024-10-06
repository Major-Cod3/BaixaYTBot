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

TOKEN = ''
URL = ''
bot = telebot.TeleBot(TOKEN, parse_mode='Markdown')


@bot.message_handler(commands=['start'])
def handle_message(message):
    bot.reply_to(message, "Olá! Bem-vindo ao nosso bot para baixar vídeos do YouTube.\n\n"
        "Para usá-lo, compartilhe o link do vídeo que deseja baixar.\n\n"
        "Para saber mais sobre o autor, use /autor.")

# Comando para mostrar informações sobre o autor
@bot.message_handler(commands=['autor'])
def send_author_info(message):
    author_info = f"""
    Eu sou Ricardo, um adolescente apaixonada por tecnologia e programação. Faço bots para Telegram por diversão e para aprender mais sobre desenvolvimento. Se você quiser saber mais sobre meus projetos ou entrar em contato, aqui estão algumas formas:
    
 - *GitHub:* https://github.com/Ricardo184
 - *instagram:* https://www.instagram.com/ricardo\_tx\_
 Obrigado por usar meu bot! :)
    """
    bot.reply_to(message, author_info)

def audio(chat, url):
	yt = YouTube(url)
	bot.send_message(chat, "Baixando Áudio...")
	audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
	audio_stream.download(output_path='download')
	files = os.listdir('download')
	for file in files:
		if file.endswith('.mp3') or file.endswith('.webm'):
			file_path = os.path.join('download', file)
			with open(file_path, 'rb') as audio_file:
				bot.send_audio(chat, audio_file, title=yt.title, performer=yt.author)
			os.remove(f'download/{file}')
			
	

def video(chat, url):
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
    markup = types.InlineKeyboardMarkup()
    
    item1 = types.InlineKeyboardButton('vídeo', callback_data='vídeo')
    
    item2 = types.InlineKeyboardButton('áudio', callback_data='áudio')
    
    markup.add(item1, item2)
    
    return markup

@bot.message_handler(func=lambda message: True)
def dowlond(mensagen):
	global URL
	padrao_youtube = r'(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([A-Za-z0-9_-]{11})'
	url_yt = re.match(padrao_youtube, f'{mensagen.text}')
	padrao_youtube_shorts = r'(?:https?://)?(?:www\.)?youtube\.com/shorts/([A-Za-z0-9_-]{11})'
	url_yt_shorts = re.match(padrao_youtube_shorts, f'{mensagen.text}')
	padrao_url = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
	
	if url_yt:
	   	URL = url_yt.group(0)
	   	bot.send_message(mensagen.chat.id, "Baixa Vídeo Como", reply_markup=inline_options())
	elif url_yt_shorts:
	   	URL = url_yt_shorts.group(0)
	   	bot.send_message(mensagen.chat.id, "Baixa Vídeo Como", reply_markup=inline_options())
		
	elif re.match(padrao_url, f'{mensagen.text}'):
		bot.reply_to(mensagen, 'Desculpe, só é possível baixar vídeos do YouTube com este bot.')
		
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    global URL
    if call.data == 'vídeo':
    	video(call.message.chat.id, URL)

    elif call.data == 'áudio':
        audio(call.message.chat.id, URL)
    bot.answer_callback_query(call.id)

bot.polling(none_stop=True)
