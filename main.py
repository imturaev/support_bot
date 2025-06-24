from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Вставь сюда свой токен
BOT_TOKEN = '7566789943:AAELXaAVS8aakElYgp3bWXQ9OGWSn0eBCNM'

# Укажи здесь Telegram ID оператора (админа)
OPERATOR_ID = 7432779827  # замени на свой Telegram user ID

# Связь user_id -> message_id оператора (чтобы понимать, кому ответить)
user_map = {}

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Здравствуйте! Напишите ваше сообщение, оператор скоро ответит.")

def handle_user_message(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    text = update.message.text
    username = update.message.from_user.username or f"ID: {user_id}"

    # Перешлем сообщение оператору
    sent = context.bot.send_message(
        chat_id=OPERATOR_ID,
        text=f"Сообщение от @{username} ({user_id}):\n{text}"
    )

    # Сохраняем соответствие между сообщением и пользователем
    user_map[sent.message_id] = user_id

def handle_operator_reply(update: Update, context: CallbackContext):
    if update.message.reply_to_message:
        orig_msg_id = update.message.reply_to_message.message_id
        if orig_msg_id in user_map:
            user_id = user_map[orig_msg_id]
            context.bot.send_message(chat_id=user_id, text=update.message.text)
        else:
            update.message.reply_text("❌ Не могу определить, кому вы отвечаете.")
    else:
        update.message.reply_text("❗ Ответьте на сообщение пользователя (reply), чтобы отправить ему сообщение.")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Обработчик команды /start
    dp.add_handler(CommandHandler("start", start))

    # Все текстовые сообщения — либо от пользователя, либо от оператора
    dp.add_handler(MessageHandler(
        Filters.text & ~Filters.command,
        lambda update, context: (
            handle_operator_reply(update, context)
            if update.message.chat_id == OPERATOR_ID
            else handle_user_message(update, context)
        )
    ))

    updater.start_polling()
    print("Бот запущен.")
    updater.idle()

if __name__ == "__main__":
    main()
