from api import create_application
from config import TOKEN
from handlers import register_start, register_chat, register_logging
from utils import configure_logging

def main() -> None:
    configure_logging()

    application = create_application(TOKEN)

    # register_logging(application)

    register_start(application)
    register_chat(application)

    application.run_polling()

if __name__ == '__main__':
    main()