import os
import requests
from dotenv import load_dotenv

load_dotenv()

def generate_image(prompt):
    enhanced_prompt = f"luxury hotel, {prompt}, ultra realistic, 4k, cinematic lighting, architecture photography"
    clean_prompt = enhanced_prompt.replace(" ", "%20")
    return f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}?width=1024&height=1024"

    return response.content  