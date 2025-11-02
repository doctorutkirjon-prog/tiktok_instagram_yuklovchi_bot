import telebot
from flask import Flask, request
import requests
import os

TOKEN = "BU_YERGA_SENING_BOT_TOKENINGNI_QOY"
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

def download_video(url):
    try:
        api_url = f"https://ssyoutube.com/api/convert?url={url}"
        response = requests.get(api_url)
        data = response.json()
        video_url = data["url"][0]["url"]
        return video_url
    except Exception as e:
        print("Xato:", e)
        return None

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🎬 Salom! Menga TikTok yoki Instagram havolasini yuboring — video tayyor holda yuklab beraman.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text.strip()
    if "tiktok.com" in url or "instagram.com" in url:
        bot.send_message(message.chat.id, "⏳ Yuklab olinmoqda, biroz kuting...")
        video_link = download_video(url)
        if video_link:
            bot.send_message(message.chat.id, "🎬 Видео тайёр!")
            bot.send_video(message.chat.id, video=video_link)
        else:
            bot.send_message(message.chat.id, "❌ Видео юклаб бўлмади. Ҳаволани текширинг.")
    else:
        bot.send_message(message.chat.id, "ℹ️ Илтимос, TikTok ёки Instagram ҳаволасини жўнатинг.")

@server.route(f"/{TOKEN}", methods=["POST"])
def getMessage():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f"https://tiktok-instagram-yuklovchi-new.onrender.com/{TOKEN}")
    return "Ishlamoqda!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))


