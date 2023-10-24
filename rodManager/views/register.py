from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import permissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class RegistrationView(APIView):
    class RegistrationView(APIView):
        permission_classes = (AllowAny,)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "password": openapi.Schema(type=openapi.TYPE_STRING),
                "first_name": openapi.Schema(type=openapi.TYPE_STRING),
                "last_name": openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=["password", "name", "surname"],
        ),
        responses={
            status.HTTP_201_CREATED: openapi.Response("Registration successful"),
            status.HTTP_400_BAD_REQUEST: openapi.Response("Bad Request"),
        },
    )
    def post(self, request):
        User = get_user_model()
        password = request.data.get("password")
        email = request.data.get("email")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")

        if not email or not password or not first_name or not last_name:
            return Response(
                {"error": "Password, email, first_name and last_name are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if validate_email(email):
            return Response(
                {"error": "Email is not valid."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "Email already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.create_user(
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        return Response(
            {"message": "Registration successful."}, status=status.HTTP_201_CREATED
        )
