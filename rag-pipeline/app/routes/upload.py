import os
import tempfile
import shutil
from fastapi import APIRouter, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from ..utils.extractors import extract_text
from ..utils.embeddings import create_vectorstore, get_embeddings
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None
):
    """Upload and process document"""
    try:
        # Validate file type
        allowed_extensions = {'.txt', '.pdf', '.docx', '.pptx'}
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": "Invalid file format",
                    "details": f"Supported formats: {', '.join(allowed_extensions)}"
                }
            )
        
        # Create temp directory
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, file.filename)
            
            # Save uploaded file
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # Extract text
            text = extract_text(file_path)
            if not text or not text.strip():
                return JSONResponse(
                    status_code=400,
                    content={
                        "success": False,
                        "error": "No text extracted",
                        "details": "File may be empty or corrupted"
                    }
                )
            
            # Create vectorstore
            vectorstore_path = os.getenv("VECTOR_DB_PATH", "./vectorstore")
            os.makedirs(vectorstore_path, exist_ok=True)
            
            embeddings = get_embeddings()
            create_vectorstore(text, embeddings, vectorstore_path)
            
            logger.info(f"Successfully processed {file.filename}")
            return JSONResponse(
                content={
                    "success": True,
                    "message": f"Document '{file.filename}' processed successfully",
                    "file_type": file_ext,
                    "chunks_created": len(text.split()) // 200  # Approximate
                }
            )
            
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Upload failed",
                "details": str(e)
            }
        )
