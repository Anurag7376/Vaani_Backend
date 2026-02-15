import os
import logging
import google.generativeai as genai

# Configure logger
logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not set.")

# Configure the Google Generative AI SDK
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the model
model = genai.GenerativeModel('gemini-1.5-flash')


def generate_ai_response(prompt: str):
    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        logger.error(f"Gemini API Error: {str(e)}", exc_info=True)
        return "AI service is temporarily unavailable."
