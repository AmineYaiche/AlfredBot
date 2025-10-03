import telebot
import yt_dlp
import os

BOT_TOKEN = os.environ.get('BOT_TOKEN')  # On va mettre le token dans Railway
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salut ! Envoie-moi un lien YouTube et je te télécharge la vidéo 🎥")

@bot.message_handler(func=lambda message: True)
def telecharger_video(message):
    url = message.text
    
    if 'youtube.com' not in url and 'youtu.be' not in url:
        bot.reply_to(message, "Envoie-moi un lien YouTube valide !")
        return
    
    bot.reply_to(message, "Téléchargement en cours... ⏳")
    
    try:
        ydl_opts = {
            'format': 'best[filesize<50M]',
            'outtmpl': '%(id)s.%(ext)s',
            'quiet': True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = f"{info['id']}.{info['ext']}"
        
        with open(filename, 'rb') as video:
            bot.send_video(message.chat.id, video)
        
        os.remove(filename)
        
    except Exception as e:
        bot.reply_to(message, f"Erreur : {str(e)}")

print("Bot démarré !")
bot.infinity_polling()