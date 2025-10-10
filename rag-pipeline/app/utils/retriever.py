import os
from langchain_community.vectorstores import FAISS
from .embeddings import get_embeddings

def get_retriever(vectorstore_path=None):
    """Get retriever from existing vectorstore"""
    if vectorstore_path is None:
        vectorstore_path = os.getenv("VECTOR_DB_PATH", "./vectorstore")
    
    try:
        embeddings = get_embeddings()
        vectorstore = FAISS.load_local(vectorstore_path, embeddings, allow_dangerous_deserialization=True)
        return vectorstore.as_retriever(search_kwargs={"k": 4})
    except Exception as e:
        print(f"Failed to load vectorstore: {e}")
        return None
