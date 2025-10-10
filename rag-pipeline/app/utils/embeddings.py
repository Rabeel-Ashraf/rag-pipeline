import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

def get_embeddings():
    """Get embeddings model with OpenAI as primary, HuggingFace as backup"""
    try:
        return OpenAIEmbeddings(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            model=os.getenv("EMBED_MODEL", "text-embedding-3-large")
        )
    except Exception as e:
        print(f"OpenAI embeddings failed, using HuggingFace: {e}")
        return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def create_vectorstore(texts, embeddings, vectorstore_path):
    """Create and save FAISS vectorstore"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    chunks = text_splitter.split_text(texts)
    
    vectorstore = FAISS.from_texts(chunks, embeddings)
    vectorstore.save_local(vectorstore_path)
    return vectorstore
