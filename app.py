import telebot
from flask import Flask, request
import requests
import os

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

# --- Видео юклаб олиш функцияси ---
def yuklab_ol(url):
    try:
        # TikTok API (янги ишлайдиган манба)
        api_url = f"https://api.tikmate.app/api/lookup?url={url}"
        javob = requests.get(api_url).json()
        if "video_url" in javob:
            return javob["video_url"]
        else:
            return None
    except Exception as e:
        print("Xato:", e)
        return None

# --- /start буйруғи ---
@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(msg, "👋 Assalomu alaykum!\nMenga TikTok yoki Instagram havolasini yuboring — 🎬 video tayyor holda qaytib beraman.")

# --- Асосий хабарни қабул қилиш ---
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.strip()

    if "tiktok.com" in text or "instagram.com" in text:
        bot.send_message(message.chat.id, "🔄 Видео тайёрланмоқда, бироз кутинг...")

        video_url = yuklab_ol(text)
        if video_url:
            try:
                bot.send_message(message.chat.id, "🎬 Видео тайёр!")
                bot.send_video(message.chat.id, video_url)
            except:
                bot.send_message(message.chat.id, "⚠️ Видео юборишда хато юз берди.")
        else:
            bot.send_message(message.chat.id, "❌ Видео топилмади. Илтимос, ҳаволани қайта текширинг.")
    else:
        bot.send_message(message.chat.id, "📎 Илтимос, фақат TikTok ёки Instagram ҳаволасини юборинг.")

# --- Webhook созламаси ---
@server.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f"https://tiktok-instagram-yuklovchi-new.onrender.com/{TOKEN}")
    return "Ishlamoqda!", 200

@server.route(f'/{TOKEN}', methods=['POST'])
def getMessage():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '', 200

# --- Ишга тушириш ---
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    server.run(host="0.0.0.0", port=port)


