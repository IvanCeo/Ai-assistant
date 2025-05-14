from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters, Application
from services.echo_service import EchoService

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply = EchoService.get_echo(update.message.text)
    await update.message.reply_text(reply)

def register_echo(app: Application):
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
    )
