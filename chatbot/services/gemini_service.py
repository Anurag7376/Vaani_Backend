import os
import logging
from typing import Optional

# Configure logger
logger = logging.getLogger(__name__)

# Safe import - only import google-genai when needed
try:
    from google import genai
    GEMINI_AVAILABLE = True
except ImportError:
    genai = None
    GEMINI_AVAILABLE = False
    logger.warning("Google Gemini SDK not installed or not available")


def get_gemini_client() -> Optional:
    """Create and return Gemini client safely"""
    if not GEMINI_AVAILABLE:
        return None

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.error("GEMINI_API_KEY environment variable not set")
        return None

    try:
        client = genai.Client(api_key=api_key)
        return client
    except Exception as e:
        logger.error(f"Failed to initialize Gemini client: {str(e)}")
        return None


def generate_ai_response(prompt: str) -> str:
    """
    Generate AI response using Google Gemini API

    Args:
        prompt (str): The input prompt for the AI

    Returns:
        str: AI generated response or fallback message
    """
    # Validate input
    if not prompt or not prompt.strip():
        logger.warning("Empty prompt provided")
        return "Please provide a valid message."

    # Check if Gemini is available
    if not GEMINI_AVAILABLE:
        logger.error("Google Gemini SDK not available")
        return "AI service is temporarily unavailable."

    # Get client
    client = get_gemini_client()
    if not client:
        return "AI service is temporarily unavailable."

    try:
        # Generate content with proper timeout and error handling
        response = client.models.generate_content(
            model="models/gemini-1.5-flash",
            contents=prompt,
            generation_config={
                "max_output_tokens": 1000,
                "temperature": 0.7,
            },
            request_options={
                "timeout": 30.0  # 30 second timeout
            }
        )

        # Extract response text
        if hasattr(response, 'text') and response.text:
            return response.text.strip()
        else:
            logger.warning("Empty response from Gemini API")
            return "I couldn't generate a response. Please try again."

    except genai.types.GoogleGenerativeAIError as e:
        logger.error(f"Gemini API error: {str(e)}")
        return "AI service is temporarily unavailable."

    except Exception as e:
        logger.error(f"Unexpected error in Gemini service: {str(e)}")
        return "AI service is temporarily unavailable."
