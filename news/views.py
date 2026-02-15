import requests
import os
from rest_framework.views import APIView
from rest_framework.response import Response


class GovtNewsView(APIView):

    def get(self, request):
        url = f"https://newsapi.org/v2/everything?q=Indian government schemes&apiKey={os.getenv('NEWS_API_KEY')}"
        response = requests.get(url)
        return Response(response.json())
