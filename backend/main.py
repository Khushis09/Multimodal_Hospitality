from fastapi import FastAPI
from llm import generate_description
from image_gen import generate_image
import base64

app = FastAPI()

@app.get("/generate")
async def generate(prompt: str):
    description = generate_description(prompt)
    image_url = generate_image(prompt)

    return {
        "description": description,
        "image": image_url
    }