from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from rest_framework.permissions import IsAuthenticated


class RegistrationView(APIView):
    def get(self, request):
        User = get_user_model()
        users = User.objects.all()
        return Response(
            {
                "users": [
                    {"username": user.username, "email": user.email} for user in users
                ]
            }
        )

    def post(self, request):
        User = get_user_model()
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")

        if not username or not password or not email:
            return Response(
                {"error": "Username, password, and email are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not validate_email(email):
            return Response(
                {"error": "Email is not valid."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.create_user(
            username=username, password=password, email=email
        )
        return Response(
            {"message": "Registration successful."}, status=status.HTTP_201_CREATED
        )
