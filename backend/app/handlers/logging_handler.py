import logging
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters, Application

logger = logging.getLogger(__name__)

async def log_update_json(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    data = update.to_dict()
    logger.info("Incoming Telegram update JSON:\n%s", data)

def register_logging(app: Application):
    app.add_handler(
        MessageHandler(filters.ALL, log_update_json),
        group=0
    )
