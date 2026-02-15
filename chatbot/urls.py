from django.urls import path, include
from .views import ChatView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from chatbot.models import ChatMessage


@api_view(['GET'])
def chat_history(request):
    if not request.user.is_authenticated:
        return Response({"error": "Login required"}, status=401)

    messages = ChatMessage.objects.filter(user=request.user)

    data = [
        {
            "message": m.message,
            "response": m.response,
            "created_at": m.created_at
        }
        for m in messages
    ]

    return Response(data)


urlpatterns = [
    path('chat/', ChatView.as_view()),
    path('history/', chat_history),
]
