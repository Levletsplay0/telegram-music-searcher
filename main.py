import telebot
from music import get_track_info, download_audio
import os


BOT_TOKEN = os.getenv("BOT_TOKEN")
print(BOT_TOKEN)

bot = telebot.TeleBot(token=BOT_TOKEN)

@bot.message_handler(commands=["start"])
def welcome(message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}! Напишите название песни или исполнителя и я вам найду её для вас!")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    track_info = get_track_info(message.text)
    if track_info:
        bot.send_photo(message.chat.id, track_info["cover_url"], caption=f"🎵 Название: {track_info['title']}\n🎤 Исполнитель: {track_info['artists']}\n💿 Альбом: {track_info['album']}\n⏱ Длительность: {track_info['duration']}\nVideo_id: {track_info['video_id']}")
        status_message = bot.send_message(message.chat.id, "Скачивание на сервере, подождите немного...")

        path = download_audio(track_info["video_id"])
        bot.delete_message(status_message.chat.id, status_message.message_id)
        
        with open(path, "rb") as audio_file:
            bot.send_audio(
                message.chat.id,
                audio_file,
                title=track_info["title"],
                performer=track_info["artists"],
                thumbnail=track_info["cover_url"]
            )
        
bot.infinity_polling()