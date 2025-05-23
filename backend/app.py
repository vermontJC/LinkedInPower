# backend/app.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google.cloud import firestore
from google.api_core.datetime_helpers import to_rfc3339
from google.auth.exceptions import DefaultCredentialsError



app = FastAPI()

# Permitir CORS desde tu frontend (ajusta la URL si usas dominio)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Cliente de Firestore
try:
    db = firestore.Client()
except DefaultCredentialsError:
    db = None

@app.get("/api/posts")
async def list_posts(limit: int = 20):
    if db is None:
        return []  # En tests o sin credenciales, devolvemos vacío
    try:
        col = (db.collection("posts")
                 .order_by("scraped_at", direction=firestore.Query.DESCENDING)
                 .limit(limit))
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
@app.get("/")
async def root():
    return {"message": "¡La API está viva! Prueba /api/posts"}
