import sqlite3

DATABASE = "support_bot.db"

conn = sqlite3.connect("support_bot.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Questions (
    question_id INTEGER PRIMARY KEY,
    problem TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS "Users Questions" (
    user_id INTEGER NOT NULL,
    username TEXT NOT NULL,
    question_id INTEGER NOT NULL,
    question TEXT NOT NULL,

    PRIMARY KEY (user_id, question_id),

    FOREIGN KEY (question_id)
        REFERENCES Questions(question_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS "Quick Questions" (
    question TEXT PRIMARY KEY,
    answer TEXT NOT NULL
)
""")

cursor.executemany(
    "INSERT OR IGNORE INTO Questions (question_id, problem) VALUES (?, ?)",
    [
        (1, "Transport"),
        (2, "Tech problem"),
        (3, "Question for specialists"),
        (4, "Other")
    ]
)

cursor.executemany(
    "INSERT OR IGNORE INTO 'Quick Questions' (question, answer) VALUES (?, ?)",
    [
        ("Как оформить заказ?", "Для оформления заказа, пожалуйста, выберите интересующий вас товар и нажмите кнопку \"Добавить в корзину\", затем перейдите в корзину и следуйте инструкциям для завершения покупки."),
        ("Как узнать статус моего заказа?", "Вы можете узнать статус вашего заказа, войдя в свой аккаунт на нашем сайте и перейдя в раздел \"Мои заказы\". Там будет указан текущий статус вашего заказа."),
        ("Как отменить заказ?", "Если вы хотите отменить заказ, пожалуйста, свяжитесь с нашей службой поддержки как можно скорее. Мы постараемся помочь вам с отменой заказа до его отправки."),
        ("Что делать, если товар пришел поврежденным?", "При получении поврежденного товара, пожалуйста, сразу свяжитесь с нашей службой поддержки и предоставьте фотографии повреждений. Мы поможем вам с обменом или возвратом товара."),
        ("Как связаться с вашей технической поддержкой?", "Вы можете связаться с нашей технической поддержкой через телефон на нашем сайте или написать нам в чат-бота."),
        ("Как узнать информацию о доставке?", "Информацию о доставке вы можете найти на странице оформления заказа на нашем сайте. Там указаны доступные способы доставки и сроки."),
        ("Другое", "-")
    ]
)


conn.commit()
conn.close()

print("support_bot.db created successfully!")