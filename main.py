import telebot
from music import get_track_info, download_audio
import os
import logging


logging.basicConfig(level=logging.INFO)


BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    logging.info("Переменная окружения BOT_TOKEN не установлена")
    raise ValueError("Переменная окружения BOT_TOKEN не установлена")

bot = telebot.TeleBot(token=BOT_TOKEN)
logging.info("Бот успешно запущен")

@bot.message_handler(commands=["start"])
def welcome(message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}! Напишите название песни или исполнителя, и я найду её для вас!")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    try:
        track_info = get_track_info(message.text)
    except Exception as e:
        logging.error(f"Ошибка поиска информации о треке: {e}")
        bot.send_message(message.chat.id, "Ошибка: не удалось найти трек.")

    if track_info:
        bot.send_photo(message.chat.id, track_info["cover_url"], caption=f"🎵 Название: {track_info['title']}\n🎤 Исполнитель: {track_info['artists']}\n💿 Альбом: {track_info['album']}\n⏱ Длительность: {track_info['duration']}\nid видео: {track_info['video_id']}")
        status_message = bot.send_message(message.chat.id, "Скачивание на сервере, подождите немного...")

        try:
            path = download_audio(track_info["video_id"])
            bot.delete_message(status_message.chat.id, status_message.message_id)
        except Exception as e:
            logging.error(f"Ошибка при скачивании аудио: {e}")
            bot.delete_message(status_message.chat.id, status_message.message_id)
            bot.send_message(message.chat.id, "Ошибка: не удалось скачать аудиофайл.")
        
        if path and os.path.exists(path):
            with open(path, "rb") as audio_file:
                bot.send_audio(
                    message.chat.id,
                    audio_file,
                    title=track_info["title"],
                    performer=track_info["artists"],
                    thumbnail=track_info["cover_url"]
                )
        else:
            bot.send_message(message.chat.id, "Ошибка: не удалось скачать аудиофайл.")
    else:
        bot.send_message(message.chat.id, "Не удалось найти трек по вашему запросу. Попробуйте еще раз с другим названием.")

bot.infinity_polling()