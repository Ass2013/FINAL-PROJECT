import telebot 
import sqlite3 
from config import TOKEN
from logic import DATABASE

bot = telebot.TeleBot(TOKEN)

db = DATABASE


@bot.message_handler(commands=['start'])
def start(message):
    with sqlite3.connect("support_bot.db") as conn:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT OR IGNORE INTO "Users Questions" (user_id, username)
            VALUES (?, ?)
        """, (message.from_user.id, message.from_user.username))
        conn.commit()
    text = (
        "Привет! Я бот для помощи в технических вопросах\n\n"
        "Commands:\n"
        "/📞 Связаться со специалистом\n"
        "/🛠 Техническая проблема\n"
        "/📚 Частые вопросы "
        "/📦 Проблема с товаром\n"
    )

@bot.message_handler(commands=['📞 Связаться со специалистом'])
def contact_specialist(message):
    pass

@bot.message_handler(commands=['🛠 Техническая проблема'])
def technical_issue(message):
    pass

@bot.message_handler(func=lambda message: message.text == '📚 Частые вопросы')
def frequently_asked_questions(message):
    import sqlite3
    from telebot import types
    conn = sqlite3.connect("support_bot.db")
    cursor = conn.cursor()
    cursor.execute('SELECT question FROM "Quick Questions"')
    questions = cursor.fetchall()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for question in questions:
        markup.add(types.KeyboardButton(question[0]))
    bot.send_message(
        message.chat.id,
        "Выберите вопрос:",
        reply_markup=markup
    )

    conn.close()

@bot.message_handler(commands=['📦 Проблема с товаром'])
def product_issue(message):
    pass

print("Bot started...")
bot.infinity_polling()