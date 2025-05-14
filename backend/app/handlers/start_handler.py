from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, Application

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Я эхо-бот. Отправь мне сообщение, и я повторю его.')

def register_start(app: Application):
    app.add_handler(CommandHandler('start', start))
