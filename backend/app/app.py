from api import create_application
from config import TOKEN
from handlers import register_start, register_echo
from utils import configure_logging

def main() -> None:
    configure_logging()

    application = create_application(TOKEN)

    register_start(application)
    register_echo(application)

    application.run_polling()

if __name__ == '__main__':
    main()