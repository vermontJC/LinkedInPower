# backend/app.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google.cloud import firestore
from google.api_core.datetime_helpers import to_rfc3339

app = FastAPI()

# Permitir CORS desde tu frontend (ajusta la URL si usas dominio)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Cliente de Firestore
db = firestore.Client()

@app.get("/api/posts")
async def list_posts(limit: int = 20):
    """
    Devuelve hasta `limit` posts, ordenados por scraped_at descendente.
    """
    try:
        col = db.collection("posts").order_by("scraped_at", direction=firestore.Query.DESCENDING).limit(limit)
        docs = col.stream()
        results = []
        for doc in docs:
            data = doc.to_dict()
            # Serializar timestamp a cadena ISO
            if "scraped_at" in data and data["scraped_at"]:
                data["scraped_at"] = to_rfc3339(data["scraped_at"])
            data["id"] = doc.id
            results.append(data)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/")
async def root():
    return {"message": "¡La API está viva! Prueba /api/posts"}
