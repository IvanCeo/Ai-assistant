import os
import requests
from backend.app.config import YANDEX_API_KEY, YANDEX_MODEL_ID, YANDEX_API_URL, YANDEX_FOLDER_ID

class YandexService:
    def complete(prompt: str) -> str:
        # Собираем запрос
        data = {}
        # Указываем тип модели
        data["modelUri"] = f"gpt://{YANDEX_FOLDER_ID}/{YANDEX_MODEL_ID}"
        # Настраиваем опции
        data["completionOptions"] = {"temperature": 0.3, "maxTokens": 1000}
        # Указываем контекст для модели
        data["messages"] = [
            {"role": "user", "text": f"{prompt}"},
        ]
    
        # Отправляем запрос
        response = requests.post(
            YANDEX_API_URL,
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {YANDEX_API_KEY}"
            },
            json=data,
        ).json()
        
        return response["result"]["alternatives"][0]["message"]["text"]
