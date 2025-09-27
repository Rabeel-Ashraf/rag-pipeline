import os
import pickle
from typing import List
from sentence_transformers import SentenceTransformer
import faiss
from .config import settings

class DocumentProcessor:
    def __init__(self):
        self.model = SentenceTransformer(settings.model_name)
        self.chunks = []
        
    def chunk_text(self, text: str) -> List[str]:
        words = text.split()
        return [' '.join(words[i:i+settings.chunk_size]) 
                for i in range(0, len(words), settings.chunk_size)]
    
    def process_directory(self, data_dir: str = "/app/data"):
        all_chunks = []
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            with open(os.path.join(data_dir, "sample.txt"), "w") as f:
                f.write("Paris is the capital of France. This RAG pipeline was built for Rabeel-Ashraf.")
        
        for filename in os.listdir(data_dir):
            if filename.endswith(".txt"):
                with open(os.path.join(data_dir, filename), "r") as f:
                    text = f.read()
                    chunks = self.chunk_text(text)
                    all_chunks.extend(chunks)
        
        if not all_chunks:
            all_chunks = ["Default document for Rabeel-Ashraf"]
        
        embeddings = self.model.encode(all_chunks)
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings.astype("float32"))
        
        os.makedirs(settings.vector_store_path, exist_ok=True)
        faiss.write_index(index, f"{settings.vector_store_path}/index.faiss")
        with open(f"{settings.vector_store_path}/chunks.pkl", "wb") as f:
            pickle.dump(all_chunks, f)
        self.chunks = all_chunks
