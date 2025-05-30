import os
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class KnowledgeBase:
    def __init__(self, kb_path="kb", cache_path="cache"):
        self.kb_path = kb_path
        self.cache_path = cache_path
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.embeddings = None
        self.metadata = None
        self.load_cache()
    
    def load_cache(self):
        try:
            with open(f"{self.cache_path}/embeddings.pkl", "rb") as f:
                self.embeddings = pickle.load(f)
            with open(f"{self.cache_path}/metadata.pkl", "rb") as f:
                self.metadata = pickle.load(f)
        except FileNotFoundError:
            self.embeddings = np.array([])
            self.metadata = []
    
    def save_cache(self):
        os.makedirs(self.cache_path, exist_ok=True)
        with open(f"{self.cache_path}/embeddings.pkl", "wb") as f:
            pickle.dump(self.embeddings, f)
        with open(f"{self.cache_path}/metadata.pkl", "wb") as f:
            pickle.dump(self.metadata, f)
    
    def process_kb(self):
        """Обход базы знаний и создание векторных представлений"""
        embeddings = []
        metadata = []
        
        for root, _, files in os.walk(self.kb_path):
            for file in files:
                if file.endswith(".txt"):
                    path = os.path.join(root, file)
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    # Разбиваем на чанки (если документ большой)
                    chunks = self._split_text(content)
                    for i, chunk in enumerate(chunks):
                        embedding = self.model.encode(chunk)
                        embeddings.append(embedding)
                        metadata.append({
                            "path": path,
                            "chunk_index": i,
                            "content": chunk,
                            "topic": os.path.relpath(root, self.kb_path)
                        })
        
        self.embeddings = np.array(embeddings)
        self.metadata = metadata
        self.save_cache()
    
    def _split_text(self, text, max_length=500):
        """Разбивает текст на чанки"""
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 > max_length:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_length = 0
            current_chunk.append(word)
            current_length += len(word) + 1
        
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        return chunks
    
    def search(self, query, topic=None, top_k=3):
        """Поиск по базе знаний"""
        query_embedding = self.model.encode(query)
        similarities = cosine_similarity(
            [query_embedding],
            self.embeddings
        )[0]
        
        # Фильтрация по теме
        if topic:
            filtered_indices = [
                i for i, meta in enumerate(self.metadata)
                if meta["topic"].startswith(topic)
            ]
            similarities_filtered = similarities[filtered_indices]
            top_indices = np.argsort(similarities_filtered)[-top_k:][::-1]
            top_indices = [filtered_indices[i] for i in top_indices]
        else:
            top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        return [self.metadata[i] for i in top_indices]