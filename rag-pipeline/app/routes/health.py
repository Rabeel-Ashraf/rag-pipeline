import os
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ..utils.retriever import get_retriever

router = APIRouter()

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        retriever = get_retriever()
        vector_count = 0
        if retriever:
            # Try to get vector count (this is approximate)
            try:
                vectorstore_path = os.getenv("VECTOR_DB_PATH", "./vectorstore")
                if os.path.exists(f"{vectorstore_path}/index.faiss"):
                    # Count files or use other method to estimate
                    vector_count = "available"
            except:
                vector_count = "unknown"
        
        return JSONResponse(
            content={
                "status": "healthy",
                "model": os.getenv("DEFAULT_MODEL", "openai"),
                "vectorstore": "loaded" if retriever else "not loaded",
                "vector_count": vector_count,
                "owner": "Rabeel-Ashraf"
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "unhealthy", "error": str(e)}
        )
