from fastapi import FastAPI
from llm import generate_description
from vector_store import add_to_vector_store, search_similar

app = FastAPI()

# ------------------ HEALTH CHECK ------------------
@app.get("/")
def health():
    return {"status": "Backend running 🚀"}

# ------------------ GENERATE ------------------
@app.get("/generate")
def generate(prompt: str):
    try:
        similar = search_similar(prompt)

        context = ""
        if similar:
            context = "Similar previous ideas:\n" + "\n".join(similar)

        enhanced_prompt = context + "\n\n" + prompt

        description = generate_description(enhanced_prompt)

        add_to_vector_store(prompt)

        return {
            "description": description,
            "image": None
        }

    except Exception as e:
        return {
            "description": f"❌ Backend Error: {str(e)}",
            "image": None
        }