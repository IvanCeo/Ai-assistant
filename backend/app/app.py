from api import create_application
from config import API_KEY_TG_BOT
from handlers import register_start, register_chat, register_logging, register_topic
from utils import configure_logging

from services import KnowledgeBase, ContextManager

def main() -> None:
    configure_logging()

    application = create_application(API_KEY_TG_BOT)
    knowledge_base = KnowledgeBase()
    knowledge_base.load_cache()
    context_manager = ContextManager()
    context_manager.load_contexts()

    # register_logging(application)

    register_start(application)
    register_chat(application, knowledge_base, context_manager)
    register_topic(application)

    application.run_polling()

if __name__ == '__main__':
    main()