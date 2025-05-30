from typing import Dict, List
from .context_manager import ContextManager
from .knowledge_base import KnowledgeBase
import time
import os
import requests
from config import YANDEX_API_KEY, YANDEX_MODEL_ID, YANDEX_API_URL, YANDEX_FOLDER_ID

class YandexService():
    def build_context_prompt(query, knowledge_items):
        context = "Актуальная информация из базы знаний:\n\n"
        for item in knowledge_items:
            context += f"Источник: {item['path']}\n"
            context += f"Контент: {item['content']}\n\n"
        return context + f"\nВопрос: {query}\nОтвет должен быть точным и основанным на предоставленной информации."
    def complete_with_knowledge(context: List[Dict[str, str]], prompt: str, new_info) -> str:
    
        context_prompt = YandexService.build_context_prompt(prompt, new_info)
        
        messages = context + [
            {"role": "system", "text": prompt + context_prompt}
        ]
        
        
        data = {}
    # Указываем тип модели
        data["modelUri"] = f"gpt://{YANDEX_FOLDER_ID}/{YANDEX_MODEL_ID}"
        # Настраиваем опции
        data["completionOptions"] = {"temperature": 0.3, "maxTokens": 1000}
        # Указываем контекст для модели
        data["messages"] = [
            {"role": "user", "text": messages},
        ]

        response = requests.post(
            YANDEX_API_URL,
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {YANDEX_API_KEY}"
            },
            json=data,
        ).json()

        print(response)
        
        reply = response["result"]["alternatives"][0]["message"]["text"]
        return reply