from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, Application
from chat_handler import chat_handler
import os

async def set_topic(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    if not context.args:
        await update.message.reply_text("Укажите тему после команды /topic")
        return
    
    topic = " ".join(context.args)
    chat_handler.set_topic(chat_id, topic)
    await update.message.reply_text(f"Тема диалога установлена: {topic}")

async def show_topic(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    current_topic = chat_handler.get_current_topic(chat_id)
    if current_topic:
        await update.message.reply_text(f"Текущая тема: {current_topic}")
    else:
        await update.message.reply_text("Тема не установлена")

async def list_topics(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    kb_path = "kb"
    topics = set()
    
    for root, _, _ in os.walk(kb_path):
        rel_path = os.path.relpath(root, kb_path)
        if rel_path != ".":
            topics.add(rel_path)
    
    if topics:
        await update.message.reply_text("Доступные темы:\n" + "\n".join(topics))
    else:
        await update.message.reply_text("Нет доступных тем")

def register_topic_handlers(app: Application):
    app.add_handler(CommandHandler("topic", set_topic))
    app.add_handler(CommandHandler("current_topic", show_topic))
    app.add_handler(CommandHandler("topics", list_topics))