import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
from .rag_engine import RAGEngine
from .document_processor import DocumentProcessor

@asynccontextmanager
async def lifespan(app: FastAPI):
    if not os.path.exists("/app/vector_store/index.faiss"):
        processor = DocumentProcessor()
        processor.process_directory()
    global rag_engine
    rag_engine = RAGEngine()
    yield

app = FastAPI(
    title="Rabeel-Ashraf's RAG Pipeline",
    lifespan=lifespan
)

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def query_rag(request: QueryRequest):
    try:
        results = await rag_engine.retrieve(request.query)
        return {"results": results, "owner": "Rabeel-Ashraf"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "owner": "Rabeel-Ashraf"}
