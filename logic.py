import sqlite3

DATABASE = "support_bot.db"

conn = sqlite3.connect("support_bot.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Cathegories (
    cathegory_id INTEGER PRIMARY KEY,
    problem TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS "Users Questions" (
    user_id INTEGER NOT NULL,
    username TEXT NOT NULL,
    cathegory_id INTEGER NOT NULL,
    question TEXT NOT NULL,

    PRIMARY KEY (user_id, cathegory_id),

    FOREIGN KEY (cathegory_id)
        REFERENCES Cathegories(cathegory_id)
)
""")


cursor.executemany(
    "INSERT OR IGNORE INTO Cathegories (cathegory_id, problem) VALUES (?, ?)",
    [
        (1, "Transport"),
        (2, "Tech problem"),
        (3, "Question for specialists"),
        (4, "Other")
    ]
)



conn.commit()
conn.close()

def save_question(message, cathegory_id):
    conn = sqlite3.connect("support_bot.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO "Users Questions" (user_id, username, cathegory_id, question)
        VALUES (?, ?, ?, ?)
    """, (message.from_user.id, message.from_user.username, cathegory_id, message.text))
    # bot.send_message(call.message.chat.id, "✅ Ваша проблема сохранена. Мы скоро ответим.")
    conn.commit()
    conn.close()

print("support_bot.db created successfully!")
