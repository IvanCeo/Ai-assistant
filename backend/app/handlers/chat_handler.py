from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters, Application
from services.yandex_service import YandexService
import logging

logger = logging.getLogger(__name__)

class ChatHandler:
    def __init__(self, yandex_service: YandexService):  # Измененный конструктор
        self.yandex_service = yandex_service
        self.user_topics = {}  # chat_id -> current_topic
    
    async def chat(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user_text = update.message.text
        chat_id = update.effective_chat.id
        current_topic = self.user_topics.get(chat_id)
        
        try:
            logger.info(f"Processing message from chat {chat_id}, topic: {current_topic}")
            reply_text = self.yandex_service.complete_with_knowledge(
                chat_id, user_text, current_topic
            )
        except Exception as e:
            logger.error(f"Request failed: {e}")
            reply_text = "Извините, произошла ошибка. Попробуйте позже."
        
        await update.message.reply_text(reply_text)
    
    def set_topic(self, chat_id, topic):
        self.user_topics[chat_id] = topic
    
    def get_current_topic(self, chat_id):
        return self.user_topics.get(chat_id)
    
    def register(self, app: Application):
        app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.chat),
            group=1
        )