from typing import Dict, List
from .context_manager import ContextManager
from .knowledge_base import KnowledgeBase
import time
import os
import requests
from config.settings import YANDEX_API_KEY, YANDEX_MODEL_ID, YANDEX_API_URL, YANDEX_FOLDER_ID

class YandexService:
    def __init__(self):
        self.knowledge_base = KnowledgeBase()
        self.context_managers: Dict[str, ContextManager] = {}
        self.default_context = ContextManager()
    
    def _get_context_manager(self, topic: str = None) -> ContextManager:
        if topic not in self.context_managers:
            self.context_managers[topic] = ContextManager(topic)
        return self.context_managers[topic]
    
    def complete_with_knowledge(self, chat_id: int, prompt: str, topic: str = None) -> str:
        context_manager = self._get_context_manager(topic)
        
        # Поиск в базе знаний
        relevant_knowledge = self.knowledge_base.search(prompt, topic)
        context_prompt = self._build_context_prompt(prompt, relevant_knowledge)
        
        # Добавляем сообщение пользователя в контекст
        context_manager.add_message(chat_id, "user", prompt)
        
        # Формируем полный контекст для модели
        messages = context_manager.get_context(chat_id) + [
            {"role": "system", "text": context_prompt}
        ]
        
        try:
            response = requests.post(
                YANDEX_API_URL,
                headers={
                    "Accept": "application/json",
                    "Authorization": f"Bearer {YANDEX_API_KEY}"
                },
                json={
                    "modelUri": f"gpt://{YANDEX_FOLDER_ID}/{YANDEX_MODEL_ID}",
                    "completionOptions": {"temperature": 0.3, "maxTokens": 1000},
                    "messages": messages
                },
            ).json()
            
            reply = response["result"]["alternatives"][0]["message"]["text"]
            context_manager.add_message(chat_id, "assistant", reply)
            return reply
        except Exception as e:
            return "Извините, произошла ошибка при обработке запроса."
    
    def _build_context_prompt(self, query, knowledge_items):
        context = "Актуальная информация из базы знаний:\n\n"
        for item in knowledge_items:
            context += f"Источник: {item['path']}\n"
            context += f"Контент: {item['content']}\n\n"
        return context + f"\nВопрос: {query}\nОтвет должен быть точным и основанным на предоставленной информации."