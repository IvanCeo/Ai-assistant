from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters, Application
from backend.app.services.yandex_service import YandexService
import logging

logger = logging.getLogger(__name__)

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text

    # Отсылаем в YandexGPT
    try:
        logger.info("Sending prompt to YandexGPT: %s", user_text)
        reply_text = YandexService.complete(user_text)
    except Exception as e:
        logger.error("YandexGPT request failed: %s", e)
        reply_text = "Извините, не могу получить ответ от модели."

    await update.message.reply_text(reply_text)

def register_chat(app: Application):
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, chat),
        # Можно оставить в группе 1, чтобы логирование (группа 0) шло раньше
        group=1
    )


