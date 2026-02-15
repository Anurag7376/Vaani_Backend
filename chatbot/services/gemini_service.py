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
# Try to find a working model - the older API might have different model names
try:
    # Try common model names that might work with older API
    model_names = [
        'models/gemini-pro',
        'gemini-pro',
        'models/text-bison-001',
        'text-bison-001',
        'models/gemini-1.0-pro-001',
        'gemini-1.0-pro-001'
    ]

    model = None
    last_error = None

    for model_name in model_names:
        try:
            model = genai.GenerativeModel(model_name)
            # Test if the model works
            test_response = model.generate_content("test")
            logger.info(f"Successfully initialized model: {model_name}")
            break
        except Exception as e:
            last_error = e
            logger.debug(f"Failed to initialize {model_name}: {str(e)[:100]}")
            continue

    if model is None:
        raise Exception(f"No working model found. Last error: {last_error}")

except Exception as e:
    logger.error(f"Failed to initialize any Gemini model: {str(e)}")
    model = None


def generate_ai_response(prompt: str):
    # Check if model is available
    if model is None:
        logger.error("No Gemini model available")
        return "AI service is temporarily unavailable."

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        logger.error(f"Gemini API Error: {str(e)}", exc_info=True)
        return "AI service is temporarily unavailable."
