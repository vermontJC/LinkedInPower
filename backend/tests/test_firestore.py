# backend/test_firestore.py
from google.cloud import firestore

def main():
    db = firestore.Client()
    doc_ref = db.collection("test").document("ping")
    doc_ref.set({"hello": "world"})
    print("Documento escrito en Firestore:", doc_ref.path)
    data = doc_ref.get().to_dict()
    print("Leído de Firestore:", data)

if __name__ == "__main__":
    main()
