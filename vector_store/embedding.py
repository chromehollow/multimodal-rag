from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')  # 384-dimensional vectors

def embed_text(text):
    return model.encode([text])[0]
