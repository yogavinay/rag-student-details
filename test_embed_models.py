import os
import requests
from dotenv import load_dotenv

os.chdir(r"c:\Users\vinay\Desktop\rag-chatbot")
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
response = requests.get(url)
data = response.json()
print("All embedding models:")
for m in data.get("models", []):
    methods = m.get("supportedGenerationMethods", [])
    if "embedContent" in methods:
        print(f" - {m['name']}")
