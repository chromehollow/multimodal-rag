# vectorstore/qdrant_handler.py
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
import uuid

model = SentenceTransformer('all-MiniLM-L6-v2')  # Embedding model
client = QdrantClient("http://localhost:6333")

COLLECTION_NAME = "rag_text_vectors"

def init_qdrant():
    if COLLECTION_NAME not in [c.name for c in client.get_collections().collections]:
        client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )

def embed_text(text):
    return model.encode([text])[0]

def upsert_text(text):
    vector = embed_text(text)
    point = PointStruct(id=str(uuid.uuid4()), vector=vector, payload={"text": text})
    client.upsert(collection_name=COLLECTION_NAME, points=[point])

def search_similar(query, top_k=3):
    query_vector = embed_text(query)
    hits = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k
    )
    return hits
