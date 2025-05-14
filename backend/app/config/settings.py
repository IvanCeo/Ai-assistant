import os

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '7748646300:AAFR7-WZqKbzyFF02JJzDu0MnUlqWwpsSZo')
YANDEX_API_KEY = os.getenv('YANDEX_API_KEY', 'your_api_key')
YANDEX_MODEL_ID = os.getenv('YANDEX_MODEL_ID', 'yandexgpt-lite')
YANDEX_FOLDER_ID = "location_folder_id"
YANDEX_API_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"