# backend/app.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google.cloud import firestore
from google.api_core.datetime_helpers import to_rfc3339
from google.auth.exceptions import DefaultCredentialsError

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Firestore client safe init
try:
    db = firestore.Client()
except DefaultCredentialsError:
    db = None

# → Nuevo endpoint para pasar test_hello
@app.get("/api/hello")
async def hello():
    return {"message": "¡Hola Mundo desde FastAPI!"}

@app.get("/api/posts")
async def list_posts(limit: int = 20):
    if db is None:
        return []
    try:
        col = (
            db.collection("posts")
              .order_by("scraped_at", direction=firestore.Query.DESCENDING)
              .limit(limit)
        )
        docs = col.stream()
        results = []
        for doc in docs:
            data = doc.to_dict()
            if data.get("scraped_at"):
                data["scraped_at"] = to_rfc3339(data["scraped_at"])
            data["id"] = doc.id
            results.append(data)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# (Opcional) raíz para comprobar despliegue
@app.get("/")
async def root():
    return {"message": "API corriendo"}