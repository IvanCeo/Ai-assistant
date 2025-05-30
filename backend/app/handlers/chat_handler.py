import logging
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters, Application
from functools import partial

from services import KnowledgeBase, YandexService, ContextManager


logger = logging.getLogger(__name__)

from functools import partial

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE, 
               knowledge_base: KnowledgeBase, context_manager: ContextManager) -> None:
    
    chat_id = update.message.chat_id
    
    user_text = update.message.text
    new_info = knowledge_base.search(user_text)
    user_context = context_manager.get_context(chat_id)

    context_manager.add_message(chat_id, "user", user_text)

    try:
        logger.info("Sending prompt to YandexGPT: %s", user_text)
        reply_text = YandexService.complete_with_knowledge(
            user_context, user_text, new_info
        )
        context_manager.add_message(chat_id, "assistant", reply_text)
    except Exception as e:
        logger.error("YandexGPT request failed: %s", e)
        reply_text = "Извините, не могу получить ответ от модели."

    await update.message.reply_text(reply_text)

def register_chat(app: Application, knowledge_base: KnowledgeBase, context_manager: ContextManager):
    chat_handler = partial(chat, knowledge_base=knowledge_base, context_manager=context_manager)
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, chat_handler),
        group=1
    )
