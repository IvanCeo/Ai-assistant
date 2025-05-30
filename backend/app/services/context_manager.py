import time
from dataclasses import dataclass, field
from typing import Dict, List
import json
import os

@dataclass
class DialogContext:
    messages: List[Dict[str, str]] = field(default_factory=list)
    last_activity: float = field(default_factory=time.time)
    metadata: Dict = field(default_factory=dict)

class ContextManager:
    def __init__(self, topic=None):
        self.topic = topic
        self.contexts: Dict[int, DialogContext] = {}  # chat_id -> context
        self.load_contexts()
    
    def _get_storage_path(self):
        os.makedirs("context_storage", exist_ok=True)
        topic_suffix = f"_{self.topic}" if self.topic else ""
        return f"context_storage/contexts{topic_suffix}.json"
    
    def load_contexts(self):
        try:
            with open(self._get_storage_path(), "r", encoding="utf-8") as f:
                data = json.load(f)
                self.contexts = {
                    int(chat_id): DialogContext(
                        messages=ctx["messages"],
                        last_activity=ctx["last_activity"],
                        metadata=ctx["metadata"]
                    )
                    for chat_id, ctx in data.items()
                }
        except (FileNotFoundError, json.JSONDecodeError):
            self.contexts = {}
    
    def save_contexts(self):
        data = {
            chat_id: {
                "messages": ctx.messages,
                "last_activity": ctx.last_activity,
                "metadata": ctx.metadata
            }
            for chat_id, ctx in self.contexts.items()
        }
        with open(self._get_storage_path(), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def init_context(self, chat_id: int):
        system_message = {
            "role": "system",
            "text": f"Ты - помощник компании Токеон. Ты должен отвечать на вопросы пользователей, основываясь на информации из базы знаний компании.  Текущая тема: {self.topic}" if self.topic 
                   else "Ты - помощник компании Токеон. Ты должен отвечать на вопросы пользователей, основываясь на информации из базы знаний компании."
        }
        self.contexts[chat_id] = DialogContext(
            messages=[system_message],
            last_activity=time.time()
        )
        self.save_contexts()
    
    def add_message(self, chat_id: int, role: str, text: str):
        if chat_id not in self.contexts:
            self.init_context(chat_id)
        
        self.contexts[chat_id].messages.append({"role": role, "text": text})
        self.contexts[chat_id].last_activity = time.time()
        
        # Ограничиваем историю сообщений
        max_history = 10
        if len(self.contexts[chat_id].messages) > max_history + 1:  # +1 для system prompt
            self.contexts[chat_id].messages = [
                self.contexts[chat_id].messages[0]] + self.contexts[chat_id].messages[-max_history:]
        
        self.save_contexts()
    
    def get_context(self, chat_id: int) -> List[Dict[str, str]]:
        if chat_id not in self.contexts:
            self.init_context(chat_id)
        return self.contexts[chat_id].messages
    
    def clear_context(self, chat_id: int):
        if chat_id in self.contexts:
            self.contexts[chat_id].messages = self.contexts[chat_id].messages[:1]  # Оставляем только system prompt
            self.save_contexts()