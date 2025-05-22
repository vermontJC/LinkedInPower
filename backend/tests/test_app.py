# backend/tests/test_app.py
from fastapi.testclient import TestClient
from backend.app import app   # ahora que backend es paquete

client = TestClient(app)

def test_hello():
    response = client.get("/api/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "¡Hola Mundo desde FastAPI!"}
