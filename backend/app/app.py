from api import create_application
from backend.app.config import API_KEY_TG_BOT
from handlers import register_start, register_chat, register_logging
from utils import configure_logging

def main() -> None:
    configure_logging()

    application = create_application(API_KEY_TG_BOT)

    # register_logging(application)

    register_start(application)
    register_chat(application)

    application.run_polling()

if __name__ == '__main__':
    main()