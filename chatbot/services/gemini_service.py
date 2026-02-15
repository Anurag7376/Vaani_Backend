import os
from google import genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not set.")

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_ai_response(prompt: str):
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt,
        )

        return response.text

    except Exception as e:
        print("Gemini Error:", str(e))
        return "AI service is temporarily unavailable."
