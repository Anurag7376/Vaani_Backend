import os
import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not set in environment variables.")

genai.configure(api_key=GEMINI_API_KEY)


def generate_ai_response(prompt: str):
    try:
        # ✅ Use stable working model
        model = genai.GenerativeModel("gemini-1.5-flash-latest")

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        print("Gemini Error:", str(e))
        return "Sorry, AI service is temporarily unavailable."
