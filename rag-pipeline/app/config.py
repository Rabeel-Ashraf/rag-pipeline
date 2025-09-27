import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    redis_host: str = os.getenv("REDIS_HOST", "localhost")
    redis_port: int = int(os.getenv("REDIS_PORT", 6379))
    model_name: str = os.getenv("MODEL_NAME", "all-MiniLM-L6-v2")
    chunk_size: int = int(os.getenv("CHUNK_SIZE", 500))
    top_k: int = int(os.getenv("TOP_K", 3))
    vector_store_path: str = "/app/vector_store"

settings = Settings()
