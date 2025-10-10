import os
import logging
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from ..utils.retriever import get_retriever
from ..utils.llm_router import call_llm_with_fallback

router = APIRouter()
logger = logging.getLogger(__name__)

class QueryRequest(BaseModel):
    query: str

@router.post("/query")
async def query_documents(request: QueryRequest):
    """Query uploaded documents"""
    try:
        retriever = get_retriever()
        if not retriever:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": "No documents uploaded",
                    "details": "Please upload documents first using /upload endpoint"
                }
            )
        
        # Retrieve relevant documents
        docs = retriever.invoke(request.query)
        context = "\n\n".join([doc.page_content for doc in docs])
        
        # Generate response with LLM fallback
        response = call_llm_with_fallback(request.query, context)
        
        logger.info(f"Query processed successfully: {request.query[:50]}...")
        return JSONResponse(
            content={
                "success": True,
                "query": request.query,
                "response": response,
                "sources": len(docs)
            }
        )
        
    except Exception as e:
        logger.error(f"Query failed: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Query processing failed",
                "details": str(e)
            }
        )
