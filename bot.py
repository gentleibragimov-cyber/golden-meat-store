import os
import telebot
from telebot import types

TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = os.environ.get("ADMIN_CHAT_ID")

if not TOKEN:
    raise ValueError("BOT_TOKEN topilmadi!")

bot = telebot.TeleBot(TOKEN)
orders = {}

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("🇺🇿 O‘zbekcha", "🇨🇦 English")
    bot.send_message(
        message.chat.id,
        "🥩 Golden Meat — Edmonton\nTilni tanlang / Choose language:",
        reply_markup=keyboard
    )

@bot.message_handler(commands=['myid'])
def myid(message):
    bot.reply_to(message, f"Sizning Telegram ID: {message.chat.id}")

@bot.message_handler(func=lambda m: m.text in ["🇺🇿 O‘zbekcha", "🇨🇦 English"])
def language(message):
    orders[message.chat.id] = {"language": message.text}
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("Қайнатилган рулет", "Дудланган рулет")
    keyboard.row("Пиширилган рулет", "Зираворли рулет")
    bot.send_message(message.chat.id, "Маҳсулот турини танланг:", reply_markup=keyboard)

@bot.message_handler(func=lambda m: m.text in [
    "Қайнатилган рулет", "Дудланган рулет",
    "Пиширилган рулет", "Зираворли рулет"
])
def product(message):
    orders.setdefault(message.chat.id, {})
    orders[message.chat.id]["product"] = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("500 грамм", "1 кг")
    bot.send_message(message.chat.id, "Оғирлигини танланг:", reply_markup=keyboard)

@bot.message_handler(func=lambda m: m.text in ["500 грамм", "1 кг"])
def weight(message):
    orders.setdefault(message.chat.id, {})
    orders[message.chat.id]["weight"] = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("🚚 Етказиб бериш", "📦 Ўзим олиб кетаман")
    bot.send_message(message.chat.id, "Қандай олишни хоҳлайсиз?", reply_markup=keyboard)

@bot.message_handler(func=lambda m: m.text in ["🚚 Етказиб бериш", "📦 Ўзим олиб кетаман"])
def delivery(message):
    orders.setdefault(message.chat.id, {})
    orders[message.chat.id]["delivery"] = message.text
    msg = bot.send_message(message.chat.id, "Исмингизни ёзинг:")
    bot.register_next_step_handler(msg, get_name)

def get_name(message):
    orders[message.chat.id]["name"] = message.text
    msg = bot.send_message(message.chat.id, "Телефон рақамингизни ёзинг:")
    bot.register_next_step_handler(msg, get_phone)

def get_phone(message):
    orders[message.chat.id]["phone"] = message.text
    msg = bot.send_message(message.chat.id, "Манзилингизни ёзинг (олиб кетиш бўлса, «Йўқ» деб ёзинг):")
    bot.register_next_step_handler(msg, get_address)

def get_address(message):
    data = orders[message.chat.id]
    data["address"] = message.text

    order_text = (
        "🛒 YANGI BUYURTMA — GOLDEN MEAT\n\n"
        f"Маҳсулот: {data['product']}\n"
        f"Оғирлиги: {data['weight']}\n"
        f"Олиш усули: {data['delivery']}\n"
        f"Исми: {data['name']}\n"
        fТелефон: {data['phone']}\n"
        f"Манзил: {data['address']}\n"
        f"Telegram ID: {message.chat.id}"
    )

    bot.send_message(message.chat.id, "✅ Буюртмангиз қабул қилинди! Нархи ва тафсилотлар тез орада тасдиқланади.")

    if ADMIN_ID:
        bot.send_message(int(ADMIN_ID), order_text)

    orders.pop(message.chat.id, None)

print("Golden Meat bot ishga tushdi!")
bot.infinity_polling()