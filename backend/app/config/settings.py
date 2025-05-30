import os
from dotenv import load_dotenv

load_dotenv()

API_KEY_TG_BOT = os.getenv('API_KEY_TG_BOT')
YANDEX_API_KEY = os.getenv('YANDEX_API_KEY')
YANDEX_MODEL_ID = os.getenv('YANDEX_MODEL_ID')
YANDEX_FOLDER_ID = os.getenv('YANDEX_FOLDER_ID')
YANDEX_API_URL = os.getenv('YANDEX_API_URL')