# 🚀 Rabeel-Ashraf's Production RAG Pipeline

High-performance Retrieval-Augmented Generation (RAG) pipeline with Docker and Kubernetes support.

## 📦 Features
- **FAISS Vector Search**: Optimized for billion-scale similarity search
- **Redis Caching**: Reduces latency for repeated queries
- **Automatic Document Ingestion**: Processes all `.txt` files in `data/` directory
- **Docker Compose**: Easy local development setup
- **Kubernetes Ready**: Production deployment manifests included
- **High Performance**: Handles 100+ requests per second
- **Customizable**: Add your own documents to the `data/` directory

## 🚀 Quick Start

### Docker (Local Development)
```bash
docker-compose up --build