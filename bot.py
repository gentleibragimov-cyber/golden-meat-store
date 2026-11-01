import os
import telebot

TOKEN = os.environ.get("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN topilmadi!")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message,
        "Assalomu alaykum! 🥩\nGolden Meat botiga xush kelibsiz!"
    )

@bot.message_handler(func=lambda message: True)
def reply(message):
    bot.reply_to(message, "Xabaringiz qabul qilindi! 😊")

print("Golden Meat bot ishga tushdi!")

bot.infinity_polling()