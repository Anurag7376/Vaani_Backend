from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterView(APIView):

    def post(self, request):
        data = request.data

        if User.objects.filter(email=data.get("email")).exists():
            return Response({"error": "Email already exists"}, status=400)

        user = User.objects.create_user(
            email=data.get("email"),
            password=data.get("password"),
            name=data.get("name"),
        )

        return Response({"message": "User created successfully"}, status=201)

