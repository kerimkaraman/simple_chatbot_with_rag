from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI-API-KEY"))

print("models to use for generate content")
for model in client.models.list():

    if "generateContent" in model.supported_actions:
        print(f"Model Adı: {model.name}")
        if hasattr(model, 'display_name'):
             print(f"Görünen Ad: {model.display_name}")
        print("-" * 20)