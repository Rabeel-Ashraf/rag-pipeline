#!/bin/bash
echo "🗑️ Removing existing vector store..."
rm -rf /app/vector_store/
echo "📚 Re-ingesting all documents..."
python -c "
import sys
sys.path.insert(0, '/app')
from app.document_processor import DocumentProcessor
processor = DocumentProcessor()
processor.process_directory()
print('✅ Re-ingestion completed!')
"
