from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Scheme
from .serializers import SchemeSerializer

class SchemeListView(APIView):
    def get(self, request):
        schemes = Scheme.objects.filter(is_active=True)
        serializer = SchemeSerializer(schemes, many=True)
        return Response(serializer.data)
