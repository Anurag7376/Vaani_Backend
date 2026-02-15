import os
import logging
from google import genai
from google.genai import types

# Configure logger
logger = logging.getLogger(__name__)

# Load API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not set.")

# 1. Initialize the modern Client
# This client handles the correct API routing automatically
client = genai.Client(api_key=GEMINI_API_KEY)

# 2. Define the Target Model
# In 2026, 'gemini-2.5-flash' is the standard stable workhorse.
# Use 'gemini-3-flash-preview' for the absolute latest.
CURRENT_MODEL = 'gemini-2.5-flash'

def generate_ai_response(prompt: str):
    try:
        # 3. Use the modern generate_content method
        response = client.models.generate_content(
            model=CURRENT_MODEL,
            contents=prompt
        )
        
        # Verify response and return text
        if response.text:
            return response.text
        return "AI generated an empty response."

    except Exception as e:
        # Catching specific API errors (Quota, Auth, etc.)
        logger.error(f"Gemini API Error: {str(e)}", exc_info=True)
        return "AI service is temporarily unavailable."