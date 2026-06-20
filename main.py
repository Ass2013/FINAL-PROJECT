import telebot
import sqlite3
from config import TOKEN
from telebot import types
from logic import DATABASE, save_question

bot = telebot.TeleBot(TOKEN)
db = DATABASE

faq_answers = {
    "delet": "Если вы хотите отменить заказ, пожалуйста, свяжитесь с нашей службой поддержки как можно скорее.",
    "order": "Для оформления заказа выберите товар, добавьте его в корзину и завершите покупку.",
    "status": "Статус заказа можно посмотреть в разделе «Мои заказы».",
    "damaged": "Если товар повреждён, отправьте фото повреждений в поддержку.",
    "support": "Связаться с поддержкой можно через сайт или этот бот.",
    "delivery": "Информация о доставке доступна при оформлении заказа.",
}


@bot.message_handler(commands=['start'])
def start(message):
    with sqlite3.connect("support_bot.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO "Users Questions" (user_id, username)
            VALUES (?, ?)
        """, (message.from_user.id, message.from_user.username))
        conn.commit()

    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("📞 Связаться со специалистом", callback_data="contact"),
        types.InlineKeyboardButton("🛠 Техническая проблема", callback_data="technical"),
        types.InlineKeyboardButton("📚 Частые вопросы", callback_data="faq"),
        types.InlineKeyboardButton("📦 Проблема с товаром", callback_data="product")
    )

    bot.send_message(
        message.chat.id,
        "Привет! Я бот для помощи в технических вопросах.\n\nВыберите действие:",
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    bot.answer_callback_query(call.id)

    if call.data == "contact":
        bot.send_message(call.message.chat.id, "📞 Опишите ваш вопрос специалисту:")
        bot.register_next_step_handler(call.message, save_question, "3")

    elif call.data == "technical":
        bot.send_message(call.message.chat.id, "🛠 Напишите вашу техническую проблему:")
        bot.register_next_step_handler(call.message, save_question, "2")

    elif call.data == "product":
        bot.send_message(call.message.chat.id, "📦 Опишите проблему с товаром:")
        bot.register_next_step_handler(call.message, save_question, "1")

    elif call.data == "faq":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("Как отменить заказ?", callback_data="delet"),
            types.InlineKeyboardButton("Как оформить заказ?", callback_data="order"),
            types.InlineKeyboardButton("Что делать, если товар пришел поврежденным?", callback_data="damaged"),
            types.InlineKeboardButton("Как узнать статус моего заказа?", callback_data="status"),
            types.InlineKeyyboardButton("Как связаться с вашей технической поддержкой?", callback_data="support"),
            types.InlineKeyboardButton("Как узнать информацию о доставке?", callback_data="delivery"),
            types.InlineKeyboardButton("Другое", callback_data="other")
        )

        bot.send_message(call.message.chat.id,"📚 Выберите вопрос:",reply_markup=markup)

    elif call.data == "other":
        bot.send_message(call.message.chat.id, "Введите ваш вопрос ниже. Он будет отправлен специалисту для рассмотрения.")
        bot.register_next_step_handler(call.message, save_question, "4")

    elif call.data in faq_answers:
        bot.send_message(call.message.chat.id, faq_answers[call.data])


print("Bot started...")
bot.infinity_polling()
