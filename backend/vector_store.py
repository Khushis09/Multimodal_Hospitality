from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Store data
texts = []
embeddings = []

# Initialize FAISS index
dimension = 384
index = faiss.IndexFlatL2(dimension)


def add_to_vector_store(text):
    global texts, embeddings

    embedding = model.encode([text])
    index.add(np.array(embedding).astype('float32'))

    texts.append(text)


def search_similar(query, top_k=2):
    if len(texts) == 0:
        return []

    query_embedding = model.encode([query])
    D, I = index.search(np.array(query_embedding).astype('float32'), top_k)

    results = [texts[i] for i in I[0] if i < len(texts)]
    return results