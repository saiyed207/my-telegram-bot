import os
import telebot
from flask import Flask
from threading import Thread
from openai import OpenAI

# 1. Get the tokens from Render Environment Variables
TELEGRAM_TOKEN = os.environ.get("BOT_TOKEN")
HF_TOKEN = os.environ.get("HF_TOKEN")

# 2. Initialize Telegram Bot and HuggingFace/OpenAI Client
bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN,
)

app = Flask(__name__)

# Dummy web server to keep it awake 24/7
@app.route('/')
def home():
    return "AI Bot is awake!"

# Bot's start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! I am an AI chatbot powered by DeepSeek-R1. Send me any message!")

# Handle all other text messages
@bot.message_handler(func=lambda message: True)
def chat_with_ai(message):
    try:
        # Show "typing..." status in Telegram
        bot.send_chat_action(message.chat.id, 'typing')

        # Send the user's message to DeepSeek AI
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1:novita",
            messages=[
                {"role": "user", "content": message.text}
            ],
        )
        
        # Get the AI's reply
        ai_reply = response.choices[0].message.content
        
        # Send it back to Telegram
        bot.reply_to(message, ai_reply)

    except Exception as e:
        bot.reply_to(message, f"Oops! The AI is having trouble right now. Error: {str(e)}")

def run():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    bot.polling(none_stop=True)
