from telegram import Update, Message
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# === НАСТРОЙКИ ===
BOT_TOKEN = '7566789943:AAELXaAVS8aakElYgp3bWXQ9OGWSn0eBCNM'
OPERATOR_CHAT_ID = 7432779827  # ID оператора (можно получить в коде через /getid)

# === /start команда ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Здравствуйте! Напишите ваше сообщение, оператор скоро ответит.")

# === Получение ID (для оператора) ===
async def getid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Ваш chat_id: {update.message.chat_id}")

# === Получение сообщений от пользователей ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text
    user_id = update.message.chat_id

    # Переслать сообщение оператору с информацией о пользователе
    await context.bot.send_message(
        chat_id=OPERATOR_CHAT_ID,
        text=f"📨 Новое сообщение от @{user.username or 'без username'} (ID: {user_id}):\n{text}"
    )

# === Ответ от оператора (формат: /reply user_id сообщение) ===
async def reply_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("❗ Используй формат: /reply user_id сообщение")
        return

    user_id = args[0]
    reply_text = ' '.join(args[1:])
    try:
        await context.bot.send_message(chat_id=int(user_id), text=reply_text)
        await update.message.reply_text("✅ Сообщение отправлено пользователю.")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка отправки: {e}")

# === Запуск бота ===
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("getid", getid))
    app.add_handler(CommandHandler("reply", reply_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен...")
    await app.run_polling()

# Запуск
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
