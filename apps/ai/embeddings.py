from sentence_transformers import SentenceTransformer
import numpy as np
_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    return _model
def embed(texts):
    embs = get_model().encode(texts, normalize_embeddings=True)
    return np.array(embs).astype("float32")
