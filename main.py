import os
import telebot
from flask import Flask
from threading import Thread

# Get the Bot token from Render Environment Variables
TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# This creates a dummy web server to keep Render happy
@app.route('/')
def home():
    return "Bot is running smoothly!"

# Bot's start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! I am alive 24/7 on Render!")

# Add more bot commands here if you want!

def run():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

if __name__ == "__main__":
    # Start the Flask web server in a separate thread
    t = Thread(target=run)
    t.start()
    # Start the Telegram bot
    bot.polling(none_stop=True)
