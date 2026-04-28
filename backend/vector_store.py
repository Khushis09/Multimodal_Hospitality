import os
import warnings
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# Suppress the warning
warnings.filterwarnings("ignore", category=UserWarning)

load_dotenv()

# Set token for HuggingFace from environment variable
HF_TOKEN = os.getenv("HF_TOKEN")
if HF_TOKEN:
    os.environ["HF_TOKEN"] = HF_TOKEN

# Load model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# In-memory storage for embeddings
stored_embeddings = []
stored_texts = []

def add_to_vector_store(text):
    """Add text to vector store"""
    embedding = model.encode(text)
    stored_embeddings.append(embedding)
    stored_texts.append(text)

def search_similar(prompt, top_k=3):
    """Search for similar texts"""
    if not stored_embeddings:
        return []
    
    query_embedding = model.encode(prompt)
    
    # Calculate cosine similarity
    from sklearn.metrics.pairwise import cosine_similarity
    similarities = cosine_similarity([query_embedding], stored_embeddings)[0]
    
    # Get top k results
    top_indices = similarities.argsort()[-top_k:][::-1]
    return [stored_texts[i] for i in top_indices if similarities[i] > 0.3]