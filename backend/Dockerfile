# backend/Dockerfile
FROM python:3.13-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8000 8080

# Ejecución: usa $PORT si existe, sino 8000
CMD exec uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}
