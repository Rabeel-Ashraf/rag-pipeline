#!/bin/bash
# Document ingestion script for Rabeel-Ashraf's RAG pipeline
VECTOR_STORE="/app/vector_store/index.faiss"

if [ ! -f "$VECTOR_STORE" ]; then
    echo "📚 Ingesting documents for Rabeel-Ashraf..."
    python -c "
import sys
sys.path.insert(0, '/app')
from app.document_processor import DocumentProcessor
processor = DocumentProcessor()
processor.process_directory()
print('✅ Ingestion completed!')
"
else
    echo "✅ Vector store already exists. Skipping ingestion."
fi
