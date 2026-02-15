from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.core.cache import cache

from schemes.services.recommender import recommend_schemes
from chatbot.services.gemini_service import generate_ai_response
from chatbot.models import ChatMessage

# Configure logger
logger = logging.getLogger(__name__)


class ChatView(APIView):
    """
    Handles both:
    - Logged-in personalized AI recommendations
    - Anonymous conversational AI with session memory
    """

    permission_classes = [AllowAny]

    def post(self, request):
        # Validate input
        message = request.data.get("message")

        if not message or not str(message).strip():
            logger.warning("Empty message received in chat request")
            return Response(
                {"error": "Message is required"},
                status=400
            )

        # Sanitize message
        message = str(message).strip()

        user = request.user if request.user.is_authenticated else None

        # ====================================================
        # CASE 1: LOGGED-IN USER → PERSONALIZED RECOMMENDATION
        # ====================================================
        if user:

            cache_key = f"chat_{user.id}_{message}"
            cached_response = cache.get(cache_key)

            if cached_response:
                return Response({"reply": cached_response})

            try:
                # Get AI recommendation
                reply = recommend_schemes(user, message)

                # Validate response
                if not reply or not str(reply).strip():
                    logger.warning(
                        "Empty response from recommendation service")
                    reply = "I couldn't generate a response. Please try again."
                else:
                    reply = str(reply).strip()

                # Save chat history in DB
                ChatMessage.objects.create(
                    user=user,
                    message=message,
                    response=reply
                )

                # Cache for 1 hour
                cache.set(cache_key, reply, timeout=3600)

                return Response({"reply": reply})

            except Exception as e:
                logger.error(f"Error in recommendation service: {str(e)}")
                return Response(
                    {"error": "Service temporarily unavailable"},
                    status=500
                )

        # ====================================================
        # CASE 2: ANONYMOUS USER → SESSION-BASED AI CHAT
        # ====================================================
        else:

            # Get existing chat history from session
            chat_history = request.session.get("chat_history", [])

            # Append user message
            chat_history.append({
                "role": "user",
                "content": message
            })

            # Build conversational prompt
            prompt = f"""
You are an AI assistant helping Indian citizens find government schemes.

Rules:
- Ask for missing details like income, state, residence type, category, age.
- Keep language simple.
- Reply in the same language the user uses.
- Guide the user step by step.

Conversation so far:
{chat_history}

Continue the conversation naturally.
"""

            try:
                reply = generate_ai_response(prompt)

                # Validate response
                if not reply or not str(reply).strip():
                    logger.warning("Empty response from Gemini service")
                    reply = "I couldn't generate a response. Please try again."
                else:
                    reply = str(reply).strip()

                # Append AI reply
                chat_history.append({
                    "role": "assistant",
                    "content": reply
                })

                # Save back to session (limit to last 10 messages)
                if len(chat_history) > 20:  # 10 user + 10 assistant messages
                    chat_history = chat_history[-20:]

                request.session["chat_history"] = chat_history

                return Response({"reply": reply})

            except Exception as e:
                logger.error(f"Error in chat service: {str(e)}")
                return Response(
                    {"error": "Service temporarily unavailable"},
                    status=500
                )


# ====================================================
# OPTIONAL: Chat History Endpoint (Logged-in Users)
# ====================================================


@api_view(['GET'])
def chat_history(request):
    if not request.user.is_authenticated:
        return Response({"error": "Login required"}, status=401)

    messages = ChatMessage.objects.filter(
        user=request.user).order_by("created_at")

    data = [
        {
            "message": m.message,
            "response": m.response,
            "created_at": m.created_at
        }
        for m in messages
    ]

    return Response(data)
