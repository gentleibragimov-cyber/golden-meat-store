
import os
import telebot
from telebot import types

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_CHAT_ID")

if not TOKEN:
    raise ValueError("BOT_TOKEN is missing. Add it to GitHub Actions Secrets.")

bot = telebot.TeleBot(TOKEN)
users = {}

# Add these image files to the GitHub repository when they are ready.
# If an image is missing, the bot will continue without it.
IMAGES = {
    "banner": "banner.jpg",
    "boiled": "boiled.jpg",
    "smoked": "smoked.jpg",
    "baked": "baked.jpg",
    "spiced": "spiced.jpg",
    "cheese": "cheese.jpg",
    "chicken": "chicken.jpg",
    "beef": "beef.jpg",
    "weight": "weights.jpg",
    "delivery": "delivery.jpg",
    "pickup": "pickup.jpg"
}

TEXT = {
    "en": {
        "welcome": "Welcome to Halal Golden Meat Online Store!\n\n"
                   "PREMIUM QUALITY. EXCEPTIONAL TASTE. GENUINE RESPECT.\n\n"
                   "We believe every customer deserves the highest quality "
                   "products and the utmost respect. Your trust is our greatest value.\n\n"
                   "It is our pleasure to serve you!",
        "choose_language": "Please choose your preferred language:",
        "method": "Please choose your preferred preparation method:",
        "boiled": "Boiled",
        "smoked": "Smoked",
        "baked": "Baked",
        "spiced": "Seasoned",
        "product": "Please select your roulade:",
        "cheese": "Cheese roulade — $40/kg",
        "chicken": "Chicken roulade — $35/kg",
        "beef": "Meat-only roulade — $45/kg",
        "weight": "Please select the quantity:",
        "order_summary": "Please review your order:",
        "method_label": "Preparation",
        "product_label": "Product",
        "weight_label": "Quantity",
        "price_label": "Price per kg",
        "total_label": "Total",
        "confirm": "Confirm order",
        "cancel": "Cancel",
        "delivery_choice": "How would you like to receive your order?",
        "delivery": "Delivery",
        "pickup": "Pickup",
        "name": "May we have your full name, please?",
        "phone": "Please enter your phone number:",
        "address": "Please enter your full delivery address:",
        "thank_you": "Thank you for choosing Halal Golden Meat!\n"
                     "Your order has been successfully sent to our team. "
                     "We will contact you shortly.",
        "admin_title": "NEW HALAL GOLDEN MEAT ORDER",
        "name_label": "Customer",
        "phone_label": "Phone",
        "address_label": "Address",
        "receiving_label": "Receiving method",
        "delivery_value": "Delivery",
        "pickup_value": "Pickup",
        "cancelled": "Your order has been cancelled. You are welcome to start again with /start.",
        "invalid": "Please use the buttons or enter the requested information.",
        "not_configured": "We are sorry. Our order system is not fully configured yet. Please contact the store directly.",
        "send_error": "We could not send your order just now. Please try again or contact the store.",
        "yes": "Yes, confirm",
        "no": "No, cancel",
        "language_saved": "Thank you. Your language has been selected."
    },
    "uz": {
        "welcome": "Halal Golden Meat онлайн дўконига хуш келибсиз!\n\n"
                   "ПРЕМИУМ СИФАТ. БЕНАЗИР ТАЪМ. ЮКСАК ҲУРМАТ.\n\n"
                   "Ҳар бир мижоз энг юқори сифатли маҳсулот ва алоҳида ҳурматга муносиб. "
                   "Сизнинг ишончингиз — биз учун энг катта қадрият.\n\n"
                   "Сизга хизмат кўрсатиш биз учун шараф!",
        "choose_language": "Илтимос, ўзингизга қулай тилни танланг:",
        "method": "Илтимос, тайёрланиш усулини танланг:",
        "boiled": "Қайнатилган",
        "smoked": "Дудланган",
        "baked": "Пиширилган",
        "spiced": "Зираворли",
        "product": "Илтимос, рулет турини танланг:",
        "cheese": "Сырли рулет — $40/кг",
        "chicken": "Товуқли рулет — $35/кг",
        "beef": "Фақат гўштли рулет — $45/кг",
        "weight": "Илтимос, миқдорни танланг:",
        "order_summary": "Илтимос, буюртмангизни текширинг:",
        "method_label": "Тайёрланиш усули",
        "product_label": "Маҳсулот",
        "weight_label": "Миқдор",
        "price_label": "1 кг нархи",
        "total_label": "Жами",
        "confirm": "Буюртмани тасдиқлаш",
        "cancel": "Бекор қилиш",
        "delivery_choice": "Буюртмангизни қандай қабул қилмоқчисиз?",
        "delivery": "Етказиб бериш",
        "pickup": "Ўзим олиб кетаман",
        "name": "Илтимос, тўлиқ исмингизни ёзинг:",
        "phone": "Илтимос, телефон рақамингизни киритинг:",
        "address": "Илтимос, етказиб бериш манзилингизни тўлиқ ёзинг:",
        "thank_you": "Halal Golden Meat'ни танлаганингиз учун катта раҳмат!\n"
                     "Буюртмангиз жамоамизга муваффақиятли юборилди. "
                     "Тез орада сиз билан боғланамиз.",
        "admin_title": "HALAL GOLDEN MEAT — ЯНГИ БУЮРТМА",
        "name_label": "Мижоз",
        "phone_label": "Телефон",
        "address_label": "Манзил",
        "receiving_label": "Олиш усули",
        "delivery_value": "Етказиб бериш",
        "pickup_value": "Олиб кетиш",
        "cancelled": "Буюртмангиз бекор қилинди. Қайта бошлаш учун /start ни босинг.",
        "invalid": "Илтимос, тугмалардан фойдаланинг ёки сўралган маълумотни киритинг.",
        "not_configured": "Узр, буюртма тизими ҳали тўлиқ созланмаган. Илтимос, дўкон билан бевосита боғланинг.",
        "send_error": "Буюртмангизни ҳозир юбориш имкони бўлмади. Қайта уриниб кўринг ёки дўкон билан боғланинг.",
        "yes": "Ҳа, тасдиқлайман",
        "no": "Йўқ, бекор қилиш",
        "language_saved": "Раҳмат. Тил танланди."
    },
    "ru": {
        "welcome": "Добро пожаловать в интернет-магазин Halal Golden Meat!\n\n"
                   "ПРЕМИАЛЬНОЕ КАЧЕСТВО. НЕПОВТОРИМЫЙ ВКУС. ИСКРЕННЕЕ УВАЖЕНИЕ.\n\n"
                   "Каждый клиент заслуживает продукции высшего качества и особого уважения. "
                   "Ваше доверие — наша главная ценность.\n\n"
                   "Для нас большая честь обслуживать вас!",
        "choose_language": "Пожалуйста, выберите удобный для вас язык:",
        "method": "Пожалуйста, выберите способ приготовления:",
        "boiled": "Варёный",
        "smoked": "Копчёный",
        "baked": "Запечённый",
        "spiced": "Со специями",
        "product": "Пожалуйста, выберите вид рулета:",
        "cheese": "Сырный рулет — $40/кг",
        "chicken": "Куриный рулет — $35/кг",
        "beef": "Рулет только из мяса — $45/кг",
        "weight": "Пожалуйста, выберите количество:",
        "order_summary": "Пожалуйста, проверьте ваш заказ:",
        "method_label": "Приготовление",
        "product_label": "Продукт",
        "weight_label": "Количество",
        "price_label": "Цена за 1 кг",
        "total_label": "Итого",
        "confirm": "Подтвердить заказ",
        "cancel": "Отменить",
        "delivery_choice": "Как вы хотели бы получить заказ?",
        "delivery": "Доставка",
        "pickup": "Самовывоз",
        "name": "Пожалуйста, введите ваше полное имя:",
        "phone": "Пожалуйста, введите номер телефона:",
        "address": "Пожалуйста, введите полный адрес доставки:",
        "thank_you": "Большое спасибо за выбор Halal Golden Meat!\n"
                     "Ваш заказ успешно отправлен нашей команде. "
                     "Мы свяжемся с вами в ближайшее время.",
        "admin_title": "HALAL GOLDEN MEAT — НОВЫЙ ЗАКАЗ",
        "name_label": "Клиент",
        "phone_label": "Телефон",
        "address_label": "Адрес",
        "receiving_label": "Способ получения",
        "delivery_value": "Доставка",
        "pickup_value": "Самовывоз",
        "cancelled": "Ваш заказ отменён. Чтобы начать заново, нажмите /start.",
        "invalid": "Пожалуйста, используйте кнопки или введите запрошенную информацию.",
        "not_configured": "Приносим извинения. Система заказов ещё не полностью настроена. Пожалуйста, свяжитесь с магазином напрямую.",
        "send_error": "Не удалось отправить заказ. Пожалуйста, попробуйте ещё раз или свяжитесь с магазином.",
        "yes": "Да, подтвердить",
        "no": "Нет, отменить",
        "language_saved": "Спасибо. Язык выбран."
    }
}

PRODUCTS = {
    "cheese": {"price": 40},
    "chicken": {"price": 35},
    "beef": {"price": 45}
}

METHOD_KEYS = ["boiled", "smoked", "baked", "spiced"]
PRODUCT_KEYS = ["cheese", "chicken", "beef"]


def get_lang(chat_id):
    return users.get(chat_id, {}).get("lang", "en")


def tr(chat_id, key):
    return TEXT[get_lang(chat_id)][key]


def make_keyboard(buttons, columns=2):
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=columns
    )
    markup.add(*[types.KeyboardButton(button) for button in buttons])
    return markup


def send_image(chat_id, image_key):
    filename = IMAGES.get(image_key)
    if filename and os.path.isfile(filename):
        try:
            with open(filename, "rb") as photo:
                bot.send_photo(chat_id, photo)
                return True
        except Exception as error:
            print("Image error:", error)
    return False


def show_methods(chat_id):
    lang = get_lang(chat_id)
    buttons = [TEXT[lang][key] for key in METHOD_KEYS]
    send_image(chat_id, "banner")
    bot.send_message(
        chat_id,
        tr(chat_id, "method"),
        reply_markup=make_keyboard(buttons)
    )
    users[chat_id]["step"] = "method"


def show_products(chat_id):
    lang = get_lang(chat_id)
    buttons = [TEXT[lang][key] for key in PRODUCT_KEYS]
    bot.send_message(
        chat_id,
        tr(chat_id, "product"),
        reply_markup=make_keyboard(buttons)
    )
    users[chat_id]["step"] = "product"


def show_weight(chat_id):
    send_image(chat_id, "weight")
    buttons = ["1 kg", "2 kg", "3 kg"]
    bot.send_message(
        chat_id,
        tr(chat_id, "weight"),
        reply_markup=make_keyboard(buttons)
    )
    users[chat_id]["step"] = "weight"


def show_summary(chat_id):
    data = users[chat_id]
    lang = get_lang(chat_id)

    method = TEXT[lang][data["method"]]
    product = TEXT[lang][data["product"]]
    weight = data["weight"]
    price = PRODUCTS[data["product"]]["price"]
    total = price * weight

    data["total"] = total

    summary = (
        f"{tr(chat_id, 'order_summary')}\n\n"
        f"{tr(chat_id, 'method_label')}: {method}\n"
        f"{tr(chat_id, 'product_label')}: {product}\n"
        f"{tr(chat_id, 'weight_label')}: {weight} kg\n"
        f"{tr(chat_id, 'price_label')}: ${price} CAD\n"
        f"{tr(chat_id, 'total_label')}: ${total} CAD"
    )

    markup = make_keyboard([
        tr(chat_id, "yes"),
        tr(chat_id, "no")
    ], columns=1)

    bot.send_message(chat_id, summary, reply_markup=markup)
    data["step"] = "confirm"


def find_choice(chat_id, message_text, keys):
    lang = get_lang(chat_id)
    for key in keys:
        if message_text == TEXT[lang][key]:
            return key
    return None


@bot.message_handler(commands=["start"])
def start(message):
    chat_id = message.chat.id
    users[chat_id] = {"step": "language"}

    send_image(chat_id, "banner")
    markup = make_keyboard(
        ["English", "O'zbekcha", "Русский"],
        columns=3
    )
    bot.send_message(
        chat_id,
        "Welcome to Halal Golden Meat Online Store!\n"
        "Please choose your language / Тилни танланг / Выберите язык:",
        reply_markup=markup
    )


@bot.message_handler(commands=["myid"])
def myid(message):
    bot.reply_to(message, f"Your Telegram ID: {message.chat.id}")


@bot.message_handler(commands=["cancel"])
def cancel(message):
    chat_id = message.chat.id
    users.pop(chat_id, None)
    bot.send_message(
        chat_id,
        "Your order has been cancelled. Use /start to begin again.",
        reply_markup=types.ReplyKeyboardRemove()
    )


@bot.message_handler(func=lambda message: True, content_types=["text"])
def handle_message(message):
    chat_id = message.chat.id
    text = message.text.strip()

    if chat_id not in users:
        users[chat_id] = {"step": "language"}

    data = users[chat_id]
    step = data.get("step", "language")

    # Language selection
    if step == "language":
        language_map = {
            "English": "en",
            "O'zbekcha": "uz",
            "Русский": "ru"
        }

        if text not in language_map:
            show_language = make_keyboard(
                ["English", "O'zbekcha", "Русский"],
                columns=3
            )
            bot.send_message(
                chat_id,
                "Please choose: English / O'zbekcha / Русский",
                reply_markup=show_language
            )
            return

        data["lang"] = language_map[text]
        data["step"] = "method"

        bot.send_message(chat_id, tr(chat_id, "welcome"))
        bot.send_message(chat_id, tr(chat_id, "language_saved"))
        show_methods(chat_id)
        return

    # Preparation method
    if step == "method":
        choice = find_choice(chat_id, text, METHOD_KEYS)
        if not choice:
            bot.send_message(chat_id, tr(chat_id, "invalid"))
            return

        data["method"] = choice
        send_image(chat_id, choice)
        show_products(chat_id)
        return

    # Product selection
    if step == "product":
        choice = find_choice(chat_id, text, PRODUCT_KEYS)
        if not choice:
            bot.send_message(chat_id, tr(chat_id, "invalid"))
            return

        data["product"] = choice
        send_image(chat_id, choice)
        show_weight(chat_id)
        return

    # Weight selection
    if step == "weight":
        weight_map = {
            "1 kg": 1,
            "2 kg": 2,
            "3 kg": 3
        }

        if text not in weight_map:
            bot.send_message(chat_id, tr(chat_id, "invalid"))
            return

        data["weight"] = weight_map[text]
        show_summary(chat_id)
        return

    # Order confirmation
    if step == "confirm":
        if text == tr(chat_id, "no"):
            users.pop(chat_id, None)
            bot.send_message(
                chat_id,
                tr(chat_id, "cancelled"),
                reply_markup=types.ReplyKeyboardRemove()
            )
            return

        if text != tr(chat_id, "yes"):
            bot.send_message(chat_id, tr(chat_id, "invalid"))
            return

        markup = make_keyboard([
            tr(chat_id, "delivery"),
            tr(chat_id, "pickup")
        ])
        send_image(chat_id, "delivery")
        bot.send_message(
            chat_id,
            tr(chat_id, "delivery_choice"),
            reply_markup=markup
        )
        data["step"] = "receiving"
        return

    # Delivery or pickup
    if step == "receiving":
        if text == tr(chat_id, "delivery"):
            data["receiving"] = "delivery"
            send_image(chat_id, "delivery")
            bot.send_message(
                chat_id,
                tr(chat_id, "name"),
                reply_markup=types.ReplyKeyboardRemove()
            )
            data["step"] = "name"
            return

        if text == tr(chat_id, "pickup"):
            data["receiving"] = "pickup"
            send_image(chat_id, "pickup")
            bot.send_message(
                chat_id,
                tr(chat_id, "name"),
                reply_markup=types.ReplyKeyboardRemove()
            )
            data["step"] = "name"
            return

        bot.send_message(chat_id, tr(chat_id, "invalid"))
        return

    # Customer name
    if step == "name":
        if len(text) < 2:
            bot.send_message(chat_id, tr(chat_id, "invalid"))
            return

        data["customer_name"] = text
        bot.send_message(chat_id, tr(chat_id, "phone"))
        data["step"] = "phone"
        return

    # Customer phone
    if step == "phone":
        if len(text) < 7:
            bot.send_message(chat_id, tr(chat_id, "invalid"))
            return

        data["phone"] = text

        if data["receiving"] == "delivery":
            bot.send_message(chat_id, tr(chat_id, "address"))
            data["step"] = "address"
        else:
            data["address"] = "Pickup"
            submit_order(chat_id)
        return

    # Delivery address
    if step == "address":
        if len(text) < 5:
            bot.send_message(chat_id, tr(chat_id, "invalid"))
            return

        data["address"] = text
        submit_order(chat_id)
        return


def submit_order(chat_id):
    data = users.get(chat_id)
    if not data:
        return

    lang = get_lang(chat_id)

    if not ADMIN_ID:
        bot.send_message(chat_id, tr(chat_id, "not_configured"))
        print("ADMIN_CHAT_ID is missing.")
        return

    method = TEXT[lang][data["method"]]
    product = TEXT[lang][data["product"]]
    price = PRODUCTS[data["product"]]["price"]
    total = data["total"]

    receiving = (
        TEXT[lang]["delivery_value"]
        if data["receiving"] == "delivery"
        else TEXT[lang]["pickup_value"]
    )

    admin_message = (
        f"{TEXT[lang]['admin_title']}\n\n"
        f"{TEXT[lang]['name_label']}: {data['customer_name']}\n"
        f"{TEXT[lang]['phone_label']}: {data['phone']}\n"
        f"{TEXT[lang]['method_label']}: {method}\n"
        f"{TEXT[lang]['product_label']}: {product}\n"
        f"{TEXT[lang]['weight_label']}: {data['weight']} kg\n"
        f"{TEXT[lang]['price_label']}: ${price} CAD\n"
        f"{TEXT[lang]['total_label']}: ${total} CAD\n"
        f"{TEXT[lang]['receiving_label']}: {receiving}\n"
        f"{TEXT[lang]['address_label']}: {data['address']}\n"
        f"Telegram ID: {chat_id}"
    )

    try:
        bot.send_message(int(ADMIN_ID), admin_message)
        bot.send_message(
            chat_id,
            tr(chat_id, "thank_you"),
            reply_markup=types.ReplyKeyboardRemove()
        )
        users.pop(chat_id, None)
    except Exception as error:
        print("Order sending error:", error)
        bot.send_message(chat_id, tr(chat_id, "send_error"))


print("Halal Golden Meat bot is running...")
bot.infinity_polling(skip_pending=True)
