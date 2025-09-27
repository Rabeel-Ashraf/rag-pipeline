import json
import pickle
import redis
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from .config import settings

class RAGEngine:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5
        )
        self.model = SentenceTransformer(settings.model_name)
        self.load_index()
    
    def load_index(self):
        index_path = f"{settings.vector_store_path}/index.faiss"
        chunks_path = f"{settings.vector_store_path}/chunks.pkl"
        self.index = faiss.read_index(index_path)
        with open(chunks_path, "rb") as f:
            self.chunks = pickle.load(f)
    
    async def retrieve(self, query: str):
        cache_key = f"rag:{abs(hash(query)) % (10**8)}"
        try:
            cached = self.redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
        except:
            pass
        
        query_vec = self.model.encode([query]).astype("float32")
        distances, indices = self.index.search(query_vec, min(settings.top_k, len(self.chunks)))
        results = [self.chunks[i] for i in indices[0]]
        
        try:
            self.redis_client.setex(cache_key, 3600, json.dumps(results))
        except:
            pass
        return results
