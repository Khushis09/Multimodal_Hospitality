import os
import requests
from dotenv import load_dotenv

load_dotenv()

def generate_image(prompt):
    enhanced_prompt = f"luxury hotel, {prompt}, ultra realistic, 4k, cinematic lighting, architecture photography"
    url = f"https://image.pollinations.ai/prompt/{enhanced_prompt.replace(' ', '%20')}?width=1024&height=1024"
    
    response = requests.get(url)
    return response.content