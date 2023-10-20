from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from rest_framework.permissions import IsAuthenticated, AllowAny


class RegistrationView(APIView):
    from rest_framework import permissions

    class RegistrationView(APIView):
        permission_classes = (AllowAny,)
        
    def post(self, request):
        User = get_user_model()
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")
        name = request.data.get("name")
        surname = request.data.get("surname")

        if not username or not password or not email or not name or not surname:
            return Response(
                {"error": "Username, password, email, name and surname are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if validate_email(email):
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
            username=username,
            password=password,
            email=email,
            first_name=name,
            last_name=surname,
        )
        return Response(
            {"message": "Registration successful."}, status=status.HTTP_201_CREATED
        )
