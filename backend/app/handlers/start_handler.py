from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, Application

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Я псевдо-бот YandexGPT. Отправб мне сообщение и я его перенаправлю на YandexGPT.')

def register_start(app: Application):
    app.add_handler(CommandHandler('start', start))
