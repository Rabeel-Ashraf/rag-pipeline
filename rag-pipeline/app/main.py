import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import upload, query, health

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Rabeel-Ashraf's Universal RAG Pipeline",
    description="Production-ready RAG backend with OpenAI + DeepSeek fallback",
    version="2.0.0"
)

# CORS middleware for Lovable/React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router, prefix="/api")
app.include_router(query.router, prefix="/api")
app.include_router(health.router, prefix="/api")

@app.get("/")
async def root():
    return {
        "message": "Welcome to Rabeel-Ashraf's Universal RAG Pipeline!",
        "docs": "/docs",
        "health": "/api/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
