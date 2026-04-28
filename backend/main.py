from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import asyncio

# Try to import modules, handle gracefully if missing
try:
    from llm import generate_description
except ImportError:
    def generate_description(prompt):
        return "Error: llm module not found"

try:
    from vector_store import add_to_vector_store, search_similar
except ImportError:
    def add_to_vector_store(prompt):
        pass
    def search_similar(prompt):
        return []

app = FastAPI()

# Add CORS middleware to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------ HEALTH CHECK ------------------
@app.get("/")
def health():
    return {"status": "Backend running 🚀"}

# ------------------ GENERATE ------------------
@app.get("/generate")
async def generate(prompt: str):
    try:
        # Run search in executor to avoid blocking
        loop = asyncio.get_event_loop()
        similar = await loop.run_in_executor(None, search_similar, prompt)

        context = ""
        if similar:
            context = "Similar previous ideas:\n" + "\n".join(similar)

        enhanced_prompt = context + "\n\n" + prompt

        # Run LLM call in executor to avoid blocking
        description = await loop.run_in_executor(None, generate_description, enhanced_prompt)

        # Store in vector store (fire and forget)
        await loop.run_in_executor(None, add_to_vector_store, prompt)

        return {
            "description": description,
            "image": None
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Backend Error: {str(e)}")