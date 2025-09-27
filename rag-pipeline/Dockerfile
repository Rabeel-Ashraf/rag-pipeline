FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chmod +x scripts/ingest.sh
RUN mkdir -p /app/vector_store
EXPOSE 8000
CMD ["sh", "-c", "./scripts/ingest.sh && uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2"]
