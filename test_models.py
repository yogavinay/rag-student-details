import os
import requests
from dotenv import load_dotenv

os.chdir(os.path.dirname(os.path.abspath(__file__)))
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("No API key found!")
else:
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        if "error" in data:
            print("Error from API:", data["error"])
        elif "models" in data:
            print("Available models:")
            for m in data["models"]:
                if "generateContent" in m.get("supportedGenerationMethods", []):
                    print(f" - {m['name']}")
        else:
            print("Response:", data)
    except Exception as e:
        print("Request failed:", e)
