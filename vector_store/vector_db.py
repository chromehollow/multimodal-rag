from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import hashlib

client = QdrantClient(host="localhost", port=6333)

def init_collection(collection_name="rag_collection", vector_size=384):
    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
        )

def embed_and_store(texts, embeddings, collection_name="rag_collection"):
    points = []
    for idx, (text, vector) in enumerate(zip(texts, embeddings)):
        uid = int(hashlib.md5(text.encode()).hexdigest(), 16) % (10 ** 12)
        points.append(PointStruct(id=uid, vector=vector, payload={"text": text}))
    
    client.upsert(collection_name=collection_name, points=points)
